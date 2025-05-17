from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PasswordFolder(models.Model):
    """
    Model representing a folder to organize passwords for a specific user.

    Attributes:
        name (str): The name of the password folder.
        user (User): The owner of the folder, linked via ForeignKey.
        created_at (datetime): Timestamp when the folder was created.
        updated_at (datetime): Timestamp when the folder was last updated.
    """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_folders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Password(models.Model):
    """
    Model representing a stored password entry associated with a user and optionally a folder.

    Attributes:
        user (User): The owner of the password entry.
        folder (PasswordFolder, optional): The folder this password belongs to; nullable.
        name (str): The display name for the password entry (e.g., service or account name).
        username (str, optional): Username for the account; optional.
        password (str): The password string itself.
        created_at (datetime): Timestamp when the password was created.
        updated_at (datetime): Timestamp when the password was last updated.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='passwords')
    folder = models.ForeignKey(PasswordFolder, on_delete=models.CASCADE, related_name='passwords', null=True, blank=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name