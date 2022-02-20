from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import logout, login
from django.contrib.auth.forms import  UserCreationForm, AuthenticationForm
from django.contrib.auth.views import  LoginView
from django.views.generic import CreateView
from .models import User
from .forms import RegisterUserForm


class RegisterUser(CreateView):
    model = User
    form_class = RegisterUserForm
    template_name = 'blog/register.html'
    success_url = 'login'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'blog/login.html'


    def get_success_url(self):
        return reverse_lazy('blog:index')


def logout_user(request):
    logout(request)
    return redirect('blog:index')