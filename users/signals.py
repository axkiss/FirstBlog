from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from users.models import ExtraUserProfile
import os


@receiver(pre_save, sender=ExtraUserProfile)
def delete_old_avatar(sender, instance, **kwargs):
    """
    Deleting old avatar if avatar of user was change
    """
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


@receiver(pre_delete, sender=ExtraUserProfile)
def delete_avatar(sender, instance, **kwargs):
    """
    Deleting avatar with the user
    """
    avatar = instance.avatar
    if avatar and os.path.isfile(avatar.path):
        os.remove(avatar.path)
