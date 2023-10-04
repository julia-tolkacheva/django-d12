from django.forms import ModelForm
from .models import Post
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models  import Group

class BasicSignupForm(SignupForm):
  def save(self, request):
    user = super(BasicSignupForm, self).save(request)
    basic_group = Group.objects.get_or_create(name='Common')[0]
    basic_group.user_set.add(user)
    return user


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