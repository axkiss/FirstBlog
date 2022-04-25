import os
import re
from io import BytesIO
from PIL import Image
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Q, F
from django.utils.html import strip_tags

from users.models import User
from django.urls import reverse
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager

from users.utils import crop_img_to_square


class Post(models.Model):
    title = models.CharField(max_length=200)
    url = models.SlugField(default='', null=False, db_index=True, max_length=80)
    description = RichTextUploadingField()
    image = models.ImageField(upload_to='post/%Y/%m/%d/',
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    thumbnail = models.ImageField(upload_to='post/%Y/%m/%d/', editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    edited_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = TaggableManager()
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse('post_detail', args=[self.url])

    def add_one_view(self):
        Post.objects.filter(id=self.id).update(views=F('views') + 1)
        return None

    @staticmethod
    def get_results_search(search_query, len_desc_post=200, posts_on_page=10, max_pages_pagination=5):
        # Find search query in database of posts
        result_posts = Post.objects.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)).order_by('-id') \
            [:posts_on_page * max_pages_pagination]
        if len(result_posts) == 0:
            return ''
        else:

            # Highlight search query in results
            for post in result_posts:

                # Remove HTML tags
                clean_desc = strip_tags(post.description)

                # Truncate description of posts
                begin = clean_desc.find(search_query)
                end = begin + len(search_query)
                if begin - len_desc_post // 2 > 0:
                    if len(clean_desc) - end < len_desc_post // 2:
                        new_begin = begin - (
                                len_desc_post // 2 - (len(clean_desc) - end)) - len_desc_post // 2
                        if new_begin < 0:
                            short_desc = clean_desc
                        else:
                            short_desc = clean_desc[new_begin:]
                    else:
                        short_desc = clean_desc[begin - len_desc_post // 2:end + len_desc_post // 2]
                else:
                    short_desc = clean_desc[:end + len_desc_post - begin]
                short_desc = '...' + short_desc.strip() + '...'

                # Highlight all the entry
                post.description = re.sub(f'({search_query})', r'<mark>\1</mark>',
                                          short_desc,
                                          flags=re.IGNORECASE)
                post.title = re.sub(f'({search_query})', r'<mark>\1</mark>',
                                    post.title, flags=re.IGNORECASE)
            return result_posts

    def create_thumbnail(self, height_side):
        # If the image of the post did not change --> break
        if self.thumbnail:
            try:
                old_image = Post.objects.get(id=self.id).image
            except ObjectDoesNotExist:
                return
            if self.image.name == old_image.name:
                return

        # Get name for thumbnail
        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        thumb_name = os.path.basename(thumb_name)
        thumb_extension = thumb_extension.lower()
        thumb_filename = thumb_name + '_thumb' + thumb_extension

        # Define image file type
        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            raise TypeError('Unrecognized image file type')

        # Open, crop and resize image
        pic = Image.open(self.image)
        pic = crop_img_to_square(pic)
        pic.thumbnail((height_side, height_side), Image.LANCZOS)

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        pic.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

    def save(self, *args, **kwargs):
        # make unique url of post
        if Post.objects.filter(Q(url=self.url) & ~Q(id=self.id)).exists():
            msec = str(timezone.now().microsecond)
            self.url = self.url[:73] + '-' + msec

        # create thumbnail from post image
        self.create_thumbnail(100)
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name')
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.text[:100]
