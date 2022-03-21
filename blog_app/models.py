from django.db import models
from users.models import User
from django.urls import reverse
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager


class Post(models.Model):
    title = models.CharField(max_length=200)
    url = models.SlugField(default='', null=False, db_index=True, max_length=80)
    description = RichTextUploadingField()
    image = models.ImageField()
    created_at = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = TaggableManager()

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse('post-detail', args=[self.url])

    def save(self, *args, **kwargs):
        # make unique url of post
        msec = str(timezone.now().microsecond)
        self.url = self.url[:73] + '-' + msec
        super(Post, self).save(*args, **kwargs)
