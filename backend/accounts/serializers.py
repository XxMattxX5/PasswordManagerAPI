from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        """
        Validate user credentials and enforce account lockout policy.

        This method:
        - Checks if the user account is currently locked and raises a PermissionDenied if so.
        - Authenticates the user manually to intercept failed attempts.
        - Increments login attempt count and applies lockout if necessary.
        - Resets login attempts on successful authentication.
        - Adds the user's encryption salt to the response payload.
        - Removes the 'refresh' token from the response for frontend-managed refresh logic.

        Raises:
            PermissionDenied: If the user's account is locked.
            ValidationError: If the credentials are invalid.
        """
        username = attrs.get('username')
        password = attrs.get('password')

        try:
             user = User.objects.select_related('profile').only(
                'id', 'username', 'password',
                'profile__locked_until', 'profile__login_attempts',
                'profile__encryption_salt',
            ).get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({'detail': 'No active account found with the given credentials'})

        profile = user.profile

        if profile.is_locked():
            raise PermissionDenied(detail="Account is temporarily locked. Please try again later.")

        if not check_password(password, user.password):
            if not profile.is_locked():
                profile.register_failed_attempt()
            raise serializers.ValidationError({'detail': 'No active account found with the given credentials'})

        refresh = RefreshToken.for_user(user)

        data = {
        'access': str(refresh.access_token),
        'encryption_salt': profile.encryption_salt,
        }

        profile.reset_login_attempts()
        
        return data
