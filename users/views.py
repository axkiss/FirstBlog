from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views import View
from .form import MyAuthenticationForm, MyUserCreationForm


class RegisterView(View):
    template_name = 'users/register.html'

    def get(self, request):
        form = MyUserCreationForm()
        context = {
            'form': form

        }
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
        context = {
            'form': form
        }
        return render(request, template_name=self.template_name, context=context)


class MyLoginView(LoginView):
    LoginView.form_class = MyAuthenticationForm
    LoginView.template_name = 'users/login.html'
