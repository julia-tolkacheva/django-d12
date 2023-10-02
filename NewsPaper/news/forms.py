from django.forms import ModelForm
from .models import Post
from django import forms

class NewsForm (ModelForm):
    class Meta:
        model = Post
        fields = ['postAuthor', 'postType', 'postCat', 'postTitle', 'postBody']
        widgets = {
          'postAuthor' : forms.Select(attrs={
            'class': 'form-control', 
          }),
          
          'postType' : forms.Select(attrs={
            'class': 'form-control', 
          }),

          'postCat' : forms.SelectMultiple(attrs={
            'class': 'form-control', 
          }),

          'postBody' : forms.Textarea(attrs={
            'class': 'form-control', 
            'placeholder': 'Здесь введите текст сообщения'
          }),

          'postTitle' : forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Введите заголовок'
          }),
        }