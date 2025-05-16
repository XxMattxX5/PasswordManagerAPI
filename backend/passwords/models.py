from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PasswordFolder(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_folders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Password(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='passwords')
    folder = models.ForeignKey(PasswordFolder, on_delete=models.CASCADE, related_name='passwords', null=True, blank=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name