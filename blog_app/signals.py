import os
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Post


@receiver(pre_save, sender=Post)
def delete_old_image_and_thumbnail(sender, instance, **kwargs):
    if not instance.id:
        return False

    try:
        old_image = sender.objects.get(id=instance.id).image
        old_thumbnail = sender.objects.get(id=instance.id).thumbnail
    except ObjectDoesNotExist:
        return False

    # compare image of post and delete the oldest image and thumbnail
    new_image = instance.image
    if old_image and old_image != new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)
        if os.path.isfile(old_thumbnail.path):
            os.remove(old_thumbnail.path)
