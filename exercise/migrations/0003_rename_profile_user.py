# Generated by Django 4.0.1 on 2022-05-02 17:35

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exercise', '0002_profile_delete_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='profile',
            new_name='user',
        ),
    ]
