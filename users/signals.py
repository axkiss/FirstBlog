from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_save
from django.dispatch import receiver
from users.models import ExtraUserProfile
import os


@receiver(pre_save, sender=ExtraUserProfile)
def delete_old_avatar(sender, instance, **kwargs):
    # not on the first creation
    if not instance.id:
        return False

    try:
        old_avatar = sender.objects.get(id=instance.id).avatar
    except ObjectDoesNotExist:
        return False

    # compare avatars and delete the oldest
    new_avatar = instance.avatar
    if old_avatar and old_avatar != new_avatar:
        if os.path.isfile(old_avatar.path):
            os.remove(old_avatar.path)


