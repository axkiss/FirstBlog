from django import forms
from ckeditor_uploader.fields import RichTextUploadingFormField
from taggit.managers import TagField
from taggit.forms import TagWidget

from blog_app.models import Comment


class AddPostForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': "form-control",
        }
        ))
    description = RichTextUploadingFormField()
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': "form-control",
            'accept': "image/*",
        }
        ))
    tag = TagField(
        widget=TagWidget(attrs={
            'class': "form-control",
        }
        ))


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
