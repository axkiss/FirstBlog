from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode

from .models import User


def check_user_and_token(user, token):
    """
    Check that a token is correct for a given user.
    Verify email of a user.
    """
    if user is not None and token_generator.check_token(user, token):
        user.email_verify = True
        return True
    return False


def add_user_to_group(user, group_name=None):
    """Get or create 'group_name' and add user to this group"""
    if group_name is not None:
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)


def get_user_by_uidb(uidb64):
    """Try to get user obj by uidb64"""
    try:
        # urlsafe_base64_decode() decodes to bytestring
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        user = None
    return user