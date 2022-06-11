import os
import re
from io import BytesIO
from PIL import Image

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.html import strip_tags
from django.core.files.base import ContentFile

from users.utils import crop_img_to_square


def get_paginate_queryset(request, queryset, page_size):
    """Make paginate queryset"""
    paginator = Paginator(queryset, page_size)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def get_results_search(model, search_query, len_desc_post=200, posts_on_page=10, max_pages_pagination=5):
    """Search for posts including a search query in the title and description"""
    # When the page is open for the first time, the search query is None
    if search_query is None:
        return ''
    search_query = search_query.strip()
    if not search_query or len(search_query) < 4:
        return ''
    # Find search query in database of posts
    result_posts = model.objects.filter(
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
            begin = clean_desc.lower().find(search_query.lower())
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


def create_thumbnail_for_post(instance, height_side=100):
    """Create a square thumbnail based of the main image"""
    # If the image of the post did not change --> break
    if instance.thumbnail:
        try:
            old_image = instance.__class__.objects.get(id=instance.id).image
        except ObjectDoesNotExist:
            return
        if instance.image.name == old_image.name:
            return

    # Get name for thumbnail
    thumb_name, thumb_extension = os.path.splitext(instance.image.name)
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
    pic = Image.open(instance.image)
    pic = crop_img_to_square(pic)
    pic.thumbnail((height_side, height_side), Image.LANCZOS)

    # Save thumbnail to in-memory file as StringIO
    temp_thumb = BytesIO()
    pic.save(temp_thumb, FTYPE)
    temp_thumb.seek(0)

    # set save=False, otherwise it will run in an infinite loop
    instance.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
    temp_thumb.close()


def get_unique_slug(instance, max_length=80):
    """Add to slug now time and make unique"""
    if instance.__class__.objects.filter(Q(slug=instance.slug) & ~Q(id=instance.id)).exists():
        msec = str(timezone.now().microsecond)
        max_length -= len(msec)
        return instance.slug[:max_length] + '-' + msec
    return instance.slug[:max_length]
