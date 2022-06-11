from django import forms
from taggit.forms import TagWidget

from .models import Comment, Post


class AddPostForm(forms.ModelForm):
    """Form for create and update post"""
    class Meta:
        model = Post
        fields = ('title', 'description', 'image', 'tag')
        widgets = {
            'title': forms.TextInput(attrs={
                'autofocus': True,
                'class': "form-control",
            }),
            'image': forms.FileInput(attrs={
                'class': "form-control",
                'accept': "image/*",
            }),
            'tag': TagWidget(attrs={
                'class': "form-control",
            })
        }


class AddCommentForm(forms.ModelForm):
    """Form for create comment to post"""
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'class': "form-control",
                'rows': 3,
            }),
        }


class FeedBackForm(forms.Form):
    """Form for sending feedback from blog"""
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'id': "name",
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': "form-control",
                'id': "email",
            }
        )
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'id': "subject",
            }
        )
    )
    main_body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': "form-control",
                'id': "subject",
                'rows': 3,
            }
        )
    )
