from django.db import models
from django.contrib.auth.models import User
import os
import base64
from datetime import timedelta
from django.utils import timezone


# Create your models here.
class Profile(models.Model):
    """
    Extends the default Django User model with additional fields for:
    - encryption salt generation,
    - login attempt tracking,
    - account lockout handling.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    encryption_salt = models.CharField(max_length=64, editable=False, blank=True)
    login_attempts = models.PositiveIntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)


    def save(self, *args, **kwargs):
        """
        Overrides the default save method to automatically generate a base64-encoded encryption salt
        if one doesn't already exist for the profile.
        """
        if not self.encryption_salt:
            salt = os.urandom(32)
            self.encryption_salt = base64.b64encode(salt).decode('utf-8')
        super().save(*args, **kwargs)

    def is_locked(self):
        """
        Checks if the user account is currently locked.
        
        Returns:
            bool: True if the account is locked and the lockout period hasn't expired, False otherwise.
        """
        return self.locked_until and self.locked_until > timezone.now()

    def register_failed_attempt(self, attempts_per_lock=5, lockout_base_minutes=15):
        """
        Increments the login attempt counter. If the number of failed attempts is a multiple
        of `attempts_per_lock`, applies a lockout penalty by setting `locked_until`.
        
        Args:
            attempts_per_lock (int): Number of failed attempts before each lockout.
            lockout_base_minutes (int): Base lockout duration in minutes. Multiplied by the lockout tier.
        """
        self.login_attempts += 1
        if self.login_attempts % attempts_per_lock == 0:
            lockout_multiplier = self.login_attempts // attempts_per_lock
            lockout_minutes = lockout_base_minutes * lockout_multiplier
            self.locked_until = timezone.now() + timedelta(minutes=lockout_minutes)
        self.save()

    def reset_login_attempts(self):
        """
        Resets the login attempt counter and removes any account lockout.
        """
        self.login_attempts = 0
        self.locked_until = None
        self.save()

    def __str__(self):
        return self.user.username

