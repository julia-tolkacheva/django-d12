from django.contrib import admin

from .models import Author, Category, Post, Comment, Subscribers, PostCategory
# Register your models here.

admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Subscribers)
admin.site.register(PostCategory)