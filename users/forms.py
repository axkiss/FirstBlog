from django import forms
from django.contrib.auth import get_user_model, password_validation, authenticate
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm, PasswordResetForm, \
    SetPasswordForm
from django.core.exceptions import ValidationError

from .models import ExtraUserProfile
from .utils import send_email_for_verify

User = get_user_model()


class MyUserCreationForm(UserCreationForm):
    """Form for registration user"""
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': "form-control",
            'placeholder': "Ivan",
        })
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'placeholder': "Ivanov",
        })
    )
    username = UsernameField(
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'placeholder': "ivan1996",
        }))
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'class': "form-control",
            'placeholder': "ivan1996@email.com",
        })
    )
    password1 = forms.CharField(
        strip=False,
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': "form-control",
        }),
    )
    password2 = forms.CharField(
        strip=False,
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': "form-control"}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")


class MyAuthenticationForm(AuthenticationForm):
    """Form for login user"""
    username = UsernameField(
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': "form-control",
            'placeholder': "Your username",
        }))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class': "form-control",
            'placeholder': "Your password",
        })
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
                # check email verify and repeat send email
                if not self.user_cache.email_verify and not self.user_cache.is_superuser:
                    send_email_for_verify(self.request, self.user_cache)
                    raise self.get_invalid_email_verify_error()

    @staticmethod
    def get_invalid_email_verify_error():
        return ValidationError(
            'Email is not verify, check your email.',
            code='invalid_login',
        )


class MyPasswordResetForm(PasswordResetForm):
    """Form for get email to reset password"""
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'autofocus': True,
            'autocomplete': 'email',
            'class': "form-control"
        })
    )


class MySetPasswordForm(SetPasswordForm):
    """Form for setting a new password"""
    new_password1 = forms.CharField(
        strip=False,
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': "form-control",
        }),
    )
    new_password2 = forms.CharField(
        strip=False,
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': "form-control"}),
    )


class EditUserForm(forms.ModelForm):
    """Form for updating main information about the user profile"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "form-control",
                                                 'required': ''}),
            'last_name': forms.TextInput(attrs={'class': "form-control",
                                                'required': ''}),
            'email': forms.EmailInput(attrs={'class': "form-control",
                                             'required': ''}),
        }


class EditExtraUserProfileForm(forms.ModelForm):
    """Form for updating extra information about the user profile"""
    class Meta:
        model = ExtraUserProfile
        fields = ('avatar', 'about_me')
        widgets = {
            'avatar': forms.FileInput(attrs={'class': "form-control",
                                             'accept': "image/*", }),
            'about_me': forms.Textarea(attrs={'class': "form-control",
                                              'rows': 3, }),
        }
