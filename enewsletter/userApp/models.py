from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
import os
from uuid import uuid4
from django.contrib.auth.models import AbstractUser, Group, Permission

def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join('image', filename)

class Department(models.Model):
    name = models.CharField(max_length=40)

class UserProfile(AbstractUser):
    regNo = models.IntegerField(unique=True, primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)

    isAdmin = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="user_profile_set",
        related_query_name="user_profile",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="user_profile_set",
        related_query_name="user_profile",
    )
class NewsLetter(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now)
    title = models.CharField(max_length=20)
    message = models.CharField(max_length=10000)
    image = models.ImageField(upload_to=upload_to)

class Bookmark(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='bookmarks')
    newsletter = models.ForeignKey(NewsLetter, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'newsletter')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.userName} bookmarked {self.newsletter.title}"

class Subscription(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
