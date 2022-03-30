from django import forms
from ckeditor_uploader.fields import RichTextUploadingFormField
from taggit.managers import TagField
from taggit.forms import TagWidget

from blog_app.models import Comment, Post


class AddPostForm(forms.ModelForm):
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
    class Meta:
        model = Comment
        fields = ('text',)

        widgets = {
            'text': forms.Textarea(attrs={
                'class': "form-control",
                'rows': 3,

            }),
        }
