from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from .forms import MyAuthenticationForm, MyUserCreationForm, MyPasswordResetForm, MySetPasswordForm, EditUserForm, \
    EditExtraUserProfileForm
from .models import User, ExtraUserProfile


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
            # Add extra profile to user
            ExtraUserProfile(user=request.user).save()
            # Add user to group 'Reader'
            group, created = Group.objects.get_or_create(name='Reader')
            request.user.groups.add(group)
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


class UserProfileView(View):
    template_name = 'users/profile.html'

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        context = {
            'user_profile': user
        }
        return render(request, template_name=self.template_name, context=context)


class EditUserProfileView(View):
    template_name = 'users/edit_profile.html'

    def get(self, request, username):
        if username == request.user.get_username():
            user = get_object_or_404(User, username=username)
            extra_user_profile, created = ExtraUserProfile.objects.get_or_create(user=user)
            main_user_form = EditUserForm(instance=user)
            extra_user_form = EditExtraUserProfileForm(instance=extra_user_profile)
            context = {
                'main_user_form': main_user_form,
                'extra_user_form': extra_user_form,
            }
            return render(request, template_name=self.template_name, context=context)
        return redirect('users:profile', username=username)

    def post(self, request, username):
        user = get_object_or_404(User, username=username)
        userprofile = get_object_or_404(ExtraUserProfile, user=user)
        main_user_form = EditUserForm(request.POST, instance=user)
        extra_user_form = EditExtraUserProfileForm(request.POST, request.FILES, instance=userprofile)
        if main_user_form.is_valid() and extra_user_form.is_valid():
            main_user_form.save()
            extra_user_form.save()
        return redirect('users:profile', username=username)
