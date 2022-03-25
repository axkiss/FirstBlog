from django.contrib.auth.models import AbstractUser, Group
from django.db import models


# Create your models here.

class User(AbstractUser):

    def has_perm_add_post(self):
        return self.has_perm('blog_app.add_post')

    def get_group(self):
        return self.groups.all().first()
