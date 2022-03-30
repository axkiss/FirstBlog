from django.contrib.auth.models import AbstractUser, Group
from django.db import models


# Create your models here.

class User(AbstractUser):

    def has_perm_add_post(self):
        return self.has_perm('blog_app.add_post')

    def has_perm_edit_post(self):
        return self.has_perm('blog_app.change_post')

    def get_group(self):
        return self.groups.all().first()


def user_directory_path(instance, filename):
    first_letter = instance.user.username[0].lower()
    return f'avatars/{first_letter}/{filename}'


class ExtraUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default=None, upload_to=user_directory_path, blank=True, null=True)
    about_me = models.TextField(default=None, max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} extra profile'
