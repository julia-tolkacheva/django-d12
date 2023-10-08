#from django.shortcuts import render

from typing import Any, Dict
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.views.generic.edit import FormView
from .models import Post, Category, Author, Subscribers
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .filters import NewsFilter
from .forms import NewsForm, SubscribeForm
from datetime import datetime
from django.utils import timezone
from django.urls import reverse_lazy
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

# LoginRequiedMixin - для авторизованного доступа к странице
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.contrib.auth.models import Group
from NewsPaper.settings import DAY_POSTS_MAX

# Create your views here.

class NewsList(ListView):
    model = Post
    #queryset = Post.objects.order_by("-postDateTime")
    ordering = ['-postDateTime']
    template_name = 'newspaper/news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context['time_now'] = timezone.localtime(timezone.now())
        context['empty'] = None
        context['filter'] = NewsFilter(self.request.GET,
                                       queryset=self.get_queryset())
        context['choices'] = Post.postChoice
        context['form'] = NewsForm()
        context['is_author'] = self.request.user.groups.filter(name='Authors').exists()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


class NewsSearch(ListView):
    queryset = Post.objects.order_by("-postDateTime")
    template_name = 'newspaper/search.html'
    context_object_name = 'news'
    paginate_by = 1

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context['time_now'] = timezone.localtime(timezone.now())
        context['empty'] = None
        context['filter'] = NewsFilter(self.request.GET,
                                       queryset=self.get_queryset())
        context['is_author'] = self.request.user.groups.filter(name='Authors').exists()

        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'newspaper/post.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context['time_now'] = timezone.localtime(timezone.now())
        context['filter'] = NewsFilter(self.request.GET,
                                       queryset=self.get_queryset())
        context['is_author'] = self.request.user.groups.filter(name='Authors').exists()
        return context

#класс представления для создания поста
class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    template_name = 'newspaper/create_post.html'
    form_class = NewsForm
    context_object_name = 'post'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        author = self.request.user.id
        dt = timezone.localtime(timezone.now())
        start = dt.replace(hour=0, minute=0, second=0, microsecond=0)

        today_posts = Post.objects.filter(postAuthor__userModel=author, postDateTime__gte=start).count()
        print(author, start, today_posts )
        context['time_now'] = timezone.localtime(timezone.now())
        context['day_post_counter'] = today_posts
        context['post_limit'] = (today_posts >= DAY_POSTS_MAX)
        return context   

    def send_email(self):
        return
        for item in self.emails.items():
            html_content = render_to_string(
                'newspaper/notification.html',
                {
                    'username': item[0],
                    'title': self.email_title,
                    'message': self.email_message,
                    'link': 'http://127.0.0.1:8000/news/'
                }
            )
            print(html_content)
            msg = EmailMultiAlternatives(
                subject=f'Новый пост в newspaper:{self.email_title}',
                body=self.email_message,
                from_email='julia.tolkacheva.666@yandex.ru',
                to=[item[1]]
            )
            msg.attach_alternative(html_content,"text/html")
            msg.send()
           
    #переопределяем обработчик формы
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        self.email_title = form.cleaned_data['postTitle']
        self.email_message = form.cleaned_data['postBody']
        
        post_cat = form.cleaned_data['postCat']
        #создаем словарь с емейлами подписчиков(чтобы не дублировать)
        self.emails = {}
        for category in post_cat:
            #по каждой категории, которая отмечена в посте, ищем подписчиков
            subscribers_qs = Subscribers.objects.all().filter(category__categoryName = category).values('subscriber')
            print (category) # [User.objects.get(id=sbs['subscriber']) for sbs in subscribers_qs])
            #каждому подписчику из списка отправляем письмо счастья
            for subscriber in subscribers_qs:
                user_obj = User.objects.get(id=subscriber['subscriber'])
                print (user_obj.email)
                username = user_obj.username
                self.emails[username]=user_obj.email
        print (self.emails.values())
        self.send_email()
        return super().form_valid(form)



#класс представления для изменения поста
class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'newspaper/create_post.html'
    form_class = NewsForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

#класс представления для удаления поста
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    template_name = 'newspaper/delete_post.html'
    queryset = Post.objects.all()
    success_url = '/news/'#reverse_lazy('newspaper:news')


#класс представления для подписки на тему
class SubscribeView(LoginRequiredMixin, FormView):
    template_name = 'newspaper/subscribe.html'
    form_class = SubscribeForm
    success_url = '/'

    def subscribe_send_mail(self, cat):
        user=self.request.user
        send_mail(
            subject=f'{user.username}, вы подписаны на обновления\
                в категории {cat}',
            message="Поздравляем!",
            from_email='julia.tolkacheva.666@yandex.ru',
            recipient_list=[user.email]
        )
        
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            print ("post! ->"+ request.POST['email'])
            cat = Category.objects.get(pk=self.kwargs.get('pk'))
            user = self.request.user
            Subscribers.objects.create(category=cat, subscriber=user)
            self.subscribe_send_mail(cat)
        return super().get(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        cat = Category.objects.get(pk=self.kwargs.get('pk'))
        user = self.request.user
        context['category'] = cat
        context['email'] = self.request.user.email
        context['is_user_already_subscribed'] = Subscribers.objects.all().filter(category=cat, subscriber=user).exists()
        context['is_author'] = self.request.user.groups.filter(name='Authors').exists()
        
        return context

#функциональное представление для включения пользователя в группу Авторы
@login_required
#только для авторизованных пользователей
def upgrade_acc(request):
    user = request.user

    author_group = Group.objects.get(name='Authors')
    if not request.user.groups.filter(name='Authors').exists():
        author_group.user_set.add(user)
        Author.objects.create(userModel=user)

    return redirect('/')

