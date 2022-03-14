from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    def get_is_staff(self):
        return self.is_staff

    def get_perm_add_post(self):
        return self.has_perm('blog_app.add_post')
