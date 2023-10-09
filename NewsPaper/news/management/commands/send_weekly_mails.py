import logging
from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.core.management.base import BaseCommand
from news.models import Post, Category, Subscribers
from django.utils import timezone
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from django.core.mail import EmailMultiAlternatives, send_mail, mail_managers

logger = logging.getLogger(__name__)

def my_job():
    def send_email(subscribers, posts, category_name):
        url=f'http://{Site.objects.get_current().domain}:8000/news'
        for item in subscribers.items():
            html_content = render_to_string(
                'newspaper/weekly_mail.html',
                {
                    'category_name': category_name,
                    'username': item[0],
                    'posts': posts,
                    'url': url,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f'Новые посты за неделю в категории:{category_name}',
                body='html',
                from_email='julia.tolkacheva.666@yandex.ru',
                to=[item[1]]
            )
            msg.attach_alternative(html_content,"text/html")
            msg.send()
            print('mails send!')
            
           

    #определяем список категорий, в которых есть подписчики
    cat_list = [cat['category'] for cat in Subscribers.objects.all().values('category')]
    #remove duplicates:
    cat_list = list(set(cat_list))
    print (cat_list)

    #определяем есть ли в категории новые посты за неделю
    start_time = timezone.localtime(timezone.now())+timezone.timedelta(days=-7)
    for cat in cat_list:
        category_name = Category.objects.get(pk=cat).categoryName
        week_posts = Post.objects.filter(postCat__pk=cat, postDateTime__gte=start_time)
        #print (cat, week_posts)
        if week_posts.exists():
            print("***")
            subscribers = Subscribers.objects.filter(category__pk=cat).values('subscriber__username','subscriber__email')
            subscribers_dict = {}
            for item in subscribers:
                subscribers_dict[item['subscriber__username']]=item['subscriber__email']
            print (subscribers_dict)
            send_email(subscribers_dict, week_posts, category_name)


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    def handle(self, *args, **options):
        scheduler=BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(),"default")
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(
                #second = "*/10",
                 day_of_week="mon", 
                 hour="00",
                 minute="00"
            ),
            id="my_job",
            max_instances=1,
            replace_existing=True
        )
        logger.info("Add job 'my_job")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", 
                hour="00",
                minute="10"
                ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler stopped successfully.")





