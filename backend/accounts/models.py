from django.db import models
from django.contrib.auth import get_user_model
import os
import base64


User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    encryption_salt = models.CharField(max_length=64, editable=False, blank=True)

    def save(self, *args, **kwargs):
        if not self.encryption_salt:
            salt = os.urandom(32)
            self.encryption_salt = base64.b64encode(salt).decode('utf-8')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

