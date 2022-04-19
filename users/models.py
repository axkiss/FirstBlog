from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.utils import make_square_img
from users.validators import ImageSizeValidator


class User(AbstractUser):
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'))
    email_verify = models.BooleanField(default=False)

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
    avatar = models.ImageField(default=None, upload_to=user_directory_path,
                               validators=[ImageSizeValidator(min_size=(65, 65), max_size=(1500, 1500))], blank=True,
                               null=True)
    about_me = models.TextField(default=None, max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} extra profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            make_square_img(150, self.avatar.path)
