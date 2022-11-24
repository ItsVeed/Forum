# authentication/models.py

from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import os
from django_resized import ResizedImageField

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('profiles/', filename)

class Role(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True, db_index=True, primary_key=True)
    email = models.EmailField(max_length=255)
    roles = models.ManyToManyField(Role, related_name='userRoles', blank=True)
    profile_pic = ResizedImageField(size=[170, 170], upload_to=get_file_path, blank=True, null=True)
    bio = models.TextField(max_length=150, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

