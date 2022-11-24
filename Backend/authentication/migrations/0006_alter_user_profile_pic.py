# Generated by Django 4.1.3 on 2022-11-07 20:22

import authentication.models
from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_user_bio_alter_user_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[300, 300], upload_to=authentication.models.get_file_path),
        ),
    ]
