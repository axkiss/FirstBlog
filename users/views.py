from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, TemplateView, FormView

from blog_app.models import SeoData
from .forms import MyAuthenticationForm, MyUserCreationForm, MyPasswordResetForm, MySetPasswordForm, EditUserForm, \
    EditExtraUserProfileForm
from .models import User, ExtraUserProfile
from .services import check_user_and_token, add_user_to_group, get_user_by_uidb
from .utils import send_email_for_verify


class MyLoginView(LoginView):
    """Login and authenticate user"""
    form_class = MyAuthenticationForm
    template_name = 'users/login.html'


class RegisterView(FormView):
    """Register, authenticate and send email for verify new user"""
    template_name = 'users/register.html'
    form_class = MyUserCreationForm
    success_url = reverse_lazy('users:email_confirm')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        send_email_for_verify(self.request, user)
        return super(RegisterView, self).form_valid(form)


class EmailConfirmView(TemplateView):
    """Show message about sending mail for verify"""
    template_name = 'users/email_confirm.html'


class EmailConfirmVerifyView(View):
    """Confirm user email or show message about an invalid link """

    def get(self, request, uidb64, token):
        user = get_user_by_uidb(uidb64)
        if check_user_and_token(user, token):
            user.save()
            login(request, user)
            add_user_to_group(user, group_name='Reader')
            return redirect('users:profile', username=user.username)
        return redirect('users:email_confirm_invalid')


class EmailConfirmInvalidView(TemplateView):
    """Show message about invalid verify"""
    template_name = 'users/email_confirm_invalid.html'


class MyPasswordResetView(PasswordResetView):
    """Show form for password reset. Processing request"""
    email_template_name = 'users/password_reset_email.html'
    seo_data = SeoData.objects.first()
    extra_email_context = {'domain': seo_data.domain, 'site_name': seo_data.site_name} if seo_data else {}
    template_name = 'users/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('users:password_reset_done')


class MyPasswordResetDoneView(PasswordResetDoneView):
    """Show a message that an instruction for password reset has been send"""
    template_name = 'users/password_reset_done.html'


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    """Show form to set new password"""
    form_class = MySetPasswordForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class MyPasswordResetCompleteView(PasswordResetCompleteView):
    """Show message about success reset password"""
    template_name = 'users/password_reset_complete.html'


class UserProfileDetailView(DetailView):
    """Show user profile"""
    template_name = 'users/profile.html'
    model = User
    context_object_name = 'user_profile'

    def get_object(self, **kwargs):
        user_objects = User.objects.all().select_related('extrauserprofile').defer('password', 'last_login',
                                                                                   'is_superuser', 'is_active',
                                                                                   'date_joined', 'email_verify')
        return get_object_or_404(user_objects, username=self.kwargs.get('username'))


class EditUserProfileView(View):
    """Show a page for updating information about the user profile"""
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

        context = {
            'main_user_form': main_user_form,
            'extra_user_form': extra_user_form,
        }
        return render(request, template_name=self.template_name, context=context)
