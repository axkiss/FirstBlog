# Generated by Django 4.0.2 on 2022-03-26 14:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraUserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, default=None, null=True, upload_to=users.models.user_directory_path, validators=[users.validators.ImageSizeValidator(max_size=(1500, 1500), min_size=(65, 65))])),
                ('about_me', models.TextField(blank=True, default=None, max_length=200, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
