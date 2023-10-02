from django_filters import FilterSet, CharFilter
from .models import Post, Author, User
from django import forms


class NewsFilter(FilterSet):
        
    #postAuthor__userModel__username = CharFilter(lookup_expr='icontains') 
    

    class Meta:
        model=Post

        fields = {
            'postDateTime' : ['gt'],
            'postAuthor' : ['exact'],
            'postTitle' : ['icontains'],
        }

        labels = {
            "postDateTime": ("Date"),
        }
        help_texts = {
            "postDateTime": ("Some useful help text."),
        }
        error_messages = {
            "postDateTime": {
                "max_length": ("This writer's name is too long."),
            },
        }


