from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from .form import MyAuthenticationForm, MyUserCreationForm, MyPasswordResetForm, MySetPasswordForm


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
    form_class = MyAuthenticationForm
    template_name = 'users/login.html'


class MyPasswordResetView(PasswordResetView):
    email_template_name = 'users/password_reset_email.html'
    template_name = 'users/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('users:password_reset_done')


class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = MySetPasswordForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'

