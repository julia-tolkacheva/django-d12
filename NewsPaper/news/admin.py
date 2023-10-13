from django.contrib import admin

from .models import Author, Category, Post, Comment, Subscribers, PostCategory
# Register your models here.

def nullRate(modeladmin, request, queryset):
    queryset.update(postRate=0)
    nullRate.short_description = 'Обнулить рейтинг поста'

def incRate(modeladmin, request, queryset):
    for obj in queryset:
        obj.postRate+=1
        obj.save()
    incRate.short_description = 'Увеличить рейтинг поста'

class PostAdmin(admin.ModelAdmin):
    #отображает поля объекта в админке
    list_display = ('postTitle','postBody','postDateTime','postRate')
    #создает фильтр
    list_filter = ('postDateTime',)
    search_fields = ('postTitle','postBody')
    #добавляет опцию в меню Action
    actions = [nullRate, incRate]

admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Subscribers)
admin.site.register(PostCategory)