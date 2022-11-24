# forum/models.py

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import m2m_changed
from authentication.models import Role

User = get_user_model()

class Section(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=False, blank=False)
    allowed_roles = models.ManyToManyField(Role, related_name='categoryRoles', blank=True)
    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.name
        
class Post(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    post = models.TextField(max_length=500, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, blank=False)
    pinned = models.BooleanField(default=False)
    datetimeuploaded = models.DateTimeField(auto_now_add=True, blank=True)
    likes = models.PositiveIntegerField(default=0, blank=True)
    users_liked = models.ManyToManyField(User, related_name='postUserLiked', blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    comment = models.TextField(max_length=500, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
    datetimeuploaded = models.DateTimeField(auto_now_add=True, blank=True)
    likes = models.PositiveIntegerField(default=0, blank=True)
    users_liked = models.ManyToManyField(User, related_name='commentUserLiked', blank=True)

    def __str__(self):
        return self.post.title + ' : ' + self.user.username

def users_liked_changed(sender, instance, action, **kwargs):
    if action == "post_add":
        instance.likes += 1
    elif action == "post_remove":
        instance.likes -= 1

m2m_changed.connect(users_liked_changed, sender=Comment.users_liked.through)
m2m_changed.connect(users_liked_changed, sender=Post.users_liked.through)