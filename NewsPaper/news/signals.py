from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives, send_mail, mail_managers
from .models import Post, Subscribers, Category, PostCategory
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

#функция обработки сигнала записи в базу данных
@receiver(m2m_changed, sender=Post.postCat.through)
def notify_subscribers_of_new_post(sender, instance, action, **kwargs):
    
    def send_email(post_instance, emails):
        for item in emails.items():
            html_content = render_to_string(
                'newspaper/notification.html',
                {
                    'post': post_instance,
                    'username': item[0],
                    'domain': Site.objects.get_current().domain,
                    'relative_url': post_instance.get_absolute_url()
                } 
            )
            msg = EmailMultiAlternatives(
                subject=f'Новый пост в newspaper:{post_instance.postTitle}',
                body=post_instance.postBody,
                from_email='julia.tolkacheva.666@yandex.ru',
                to=[item[1]]
            )
            msg.attach_alternative(html_content,"text/html")
            msg.send()
            print(f'username:{item[0]}-email:{item[1]}')
 

    if action == 'post_add':
        subscribers= instance.postCat.values(
            'subscriber__email', 'subscriber__username')

        #создаем словарь с емейлами подписчиков(чтобы не дублировать)
        emails = {}

        for subscriber in subscribers:
            username = subscriber.get("subscriber__username")
            email = subscriber.get('subscriber__email')
            if email:
                emails[username]=email

        send_email(instance, emails)

            # domain = Site.objects.get_current().domain,
            # post_url = instance.get_absolute_url()
            # print(f'{type(post)}-{username}-{email}-{domain}-{post_url}')
        # email_title = instance.postTitle
        # email_message = instance.postBody
        # post_author = instance.postAuthor
        # print(type(instance))
        # post_cat = PostCategory.objects.all()
        # leng=len(post_cat)-1


        # print(f'test:{email_title}-{email_message}-{post_author}-{instance.id}-{post_cat[leng]}')
    # #создаем словарь с емейлами подписчиков(чтобы не дублировать)
    # emails = {}
    # for category in post_cat:
    #     #по каждой категории, которая отмечена в посте, ищем подписчиков
    #     subscribers_qs = Subscribers.objects.all().filter(category__categoryName = category).values('subscriber')
    #     print (category) 
    #     #каждому подписчику из списка отправляем письмо счастья
    #     for subscriber in subscribers_qs:
    #         user_obj = User.objects.get(id=subscriber['subscriber'])
    #         print (user_obj.email)
    #         username = user_obj.username
    #         emails[username]=user_obj.email
    # print (emails.values())
    # send_email(email_title, email_message, emails)

