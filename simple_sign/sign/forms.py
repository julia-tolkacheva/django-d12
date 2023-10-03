from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django import forms

class RegisterForm(UserCreationForm):
    password1 = forms.CharField(max_length=16, 
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                label='Придумайте пароль:')
    password2 = forms.CharField(max_length=16, 
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                label='Повторите пароль:')
    
    class Meta:
        model = User
        fields = ('username',
                 'email',
                 'password1',
                 'password2',
                 )
        widgets = {
            'username' : forms.TextInput(attrs={'class': 'form-control'}),
            'email' : forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if User.objects.filter(username = username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует")
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return super().clean()
    
        
