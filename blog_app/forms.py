from ckeditor_uploader.fields import RichTextUploadingFormField
from django import forms


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
