from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import RegisterForm

class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'sign/register.html'
    success_url = '/'
