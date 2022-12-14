# Generated by Django 4.1.3 on 2022-11-06 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_role_user_roles'),
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='staff_only',
        ),
        migrations.AddField(
            model_name='category',
            name='allowed_roles',
            field=models.ManyToManyField(blank=True, related_name='categoryRoles', to='authentication.role'),
        ),
    ]
