from django.db import models
from django.contrib.auth.models import User
import os
import base64
from datetime import timedelta
from django.utils import timezone


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    encryption_salt = models.CharField(max_length=64, editable=False, blank=True)
    login_attempts = models.PositiveIntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.encryption_salt:
            salt = os.urandom(32)
            self.encryption_salt = base64.b64encode(salt).decode('utf-8')
        super().save(*args, **kwargs)

    def is_locked(self):
        return self.locked_until and self.locked_until > timezone.now()

    def register_failed_attempt(self, attempts_per_lock=5, lockout_base_minutes=15):
        self.login_attempts += 1
        if self.login_attempts % attempts_per_lock == 0:
            lockout_multiplier = self.login_attempts // attempts_per_lock
            lockout_minutes = lockout_base_minutes * lockout_multiplier
            self.locked_until = timezone.now() + timedelta(minutes=lockout_minutes)
        self.save()

    def reset_login_attempts(self):
        self.login_attempts = 0
        self.locked_until = None
        self.save()

    def __str__(self):
        return self.user.username

