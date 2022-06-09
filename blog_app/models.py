from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import F
from blog_app.services import create_thumbnail_for_post, get_unique_slug
from users.models import User
from django.urls import reverse
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from users.validators import ImageSizeValidator


class SeoData(models.Model):
    """Seo data of blog"""
    site_name = models.CharField(max_length=80)
    domain = models.CharField(max_length=80, help_text='For example: test.com')
    favicon = models.ImageField(validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'ico']),
                                            ImageSizeValidator(min_size=(16, 16), max_size=(144, 144))])
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=140)

    def __str__(self):
        return self.title

    def clean(self):
        # Only 1 record
        if SeoData.objects.count() > 0 and self.id != SeoData.objects.get().id:
            raise ValidationError('You can not add new records, you can only change the existing.')


class Post(models.Model):
    """Posts on blog"""
    title = models.CharField(max_length=100)
    slug = models.SlugField(default='', null=False, db_index=True, max_length=80)
    description = RichTextUploadingField()
    image = models.ImageField(upload_to='post/%Y/%m/%d/',
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
                                          ImageSizeValidator(min_size=(1200, 900), max_size=(4000, 3000))])
    thumbnail = models.ImageField(upload_to='post/%Y/%m/%d/', editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    edited_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = TaggableManager()
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])

    def add_one_view(self):
        Post.objects.filter(id=self.id).update(views=F('views') + 1)
        return None

    def save(self, *args, **kwargs):
        # make unique slug of post
        self.slug = get_unique_slug(self, max_length=80)

        # create thumbnail from post image
        create_thumbnail_for_post(self, height_side=100)
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    """Comments under the post"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name')
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.text[:100]
