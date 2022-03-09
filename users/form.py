from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms


class MyAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': "form-control",
            'placeholder': "Your username",
        }))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class': "form-control",
            'placeholder': "Your password",
        })
    )
