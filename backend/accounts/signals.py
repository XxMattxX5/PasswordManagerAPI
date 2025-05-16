# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile
import os
import base64

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Generate a random salt
        salt = base64.b64encode(os.urandom(32)).decode('utf-8')
        # Create profile with salt
        Profile.objects.create(user=instance, encryption_salt=salt)