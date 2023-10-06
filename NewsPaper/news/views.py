#from django.shortcuts import render

from typing import Any, Dict
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.views.generic.edit import FormView
from .models import Post, Category, Author, Subscribers
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .filters import NewsFilter
from .forms import NewsForm, SubscribeForm
from datetime import datetime
from django.utils import timezone
from django.urls import reverse_lazy

# LoginRequiedMixin - для авторизованного доступа к странице
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.contrib.auth.models import Group

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

class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    template_name = 'newspaper/create_post.html'
    form_class = NewsForm

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

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            print ("post! ->"+ request.POST['email'])
            cat = Category.objects.get(pk=self.kwargs.get('pk'))
            user = self.request.user
            Subscribers.objects.create(category=cat, subscriber=user)
            form.send_email()
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

