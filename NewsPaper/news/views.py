#from django.shortcuts import render

from typing import Any, Dict
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Post
from django.shortcuts import render
from django.core.paginator import Paginator
from .filters import NewsFilter
from .forms import NewsForm # импортируем нашу форму
from datetime import datetime
from django.utils import timezone
from django.urls import reverse_lazy

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

        return context



class NewsDetail(DetailView):
    model = Post
    template_name = 'newspaper/post.html'
    context_object_name = 'post'

class PostCreateView(CreateView):
    template_name = 'newspaper/create_post.html'
    form_class = NewsForm

class PostUpdateView(UpdateView):
    template_name = 'newspaper/create_post.html'
    form_class = NewsForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDeleteView(DeleteView):
    template_name = 'newspaper/delete_post.html'
    queryset = Post.objects.all()
    success_url = '../../news/'#reverse_lazy('newspaper:news')


