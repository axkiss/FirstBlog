from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import ExtraUserProfile

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    pass


@admin.register(ExtraUserProfile)
class ExtraUserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'about_me')