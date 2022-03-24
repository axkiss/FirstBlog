from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):

    def has_perm_add_post(self):
        return self.has_perm('blog_app.add_post')
