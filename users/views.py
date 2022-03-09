from django.contrib.auth.views import LoginView
from django.shortcuts import render


# Create your views here.
from .form import MyAuthenticationForm


class MyLoginView(LoginView):
    LoginView.form_class = MyAuthenticationForm
    LoginView.template_name = 'users/login.html'


