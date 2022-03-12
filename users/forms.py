from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm, PasswordResetForm, \
    SetPasswordForm
from django import forms
from django.utils.translation import gettext, gettext_lazy as _

User = get_user_model()


class MyUserCreationForm(UserCreationForm):
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
        fields = ("first_name", "last_name", "username", "email")


class MyAuthenticationForm(AuthenticationForm):
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


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'autofocus': True,
            'autocomplete': 'email',
            'class': "form-control"
        })
    )


class MySetPasswordForm(SetPasswordForm):
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
