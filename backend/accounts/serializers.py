from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = User.objects.filter(username=username).first()

        if user and hasattr(user, 'profile'):
            profile = user.profile
            if profile.is_locked():
                raise PermissionDenied(detail={"time": profile.locked_until.isoformat()})

        # Authenticate manually to check password before calling super().validate
        user = authenticate(username=username, password=password)
        if not user:
            # Bad password but valid username
            user = User.objects.filter(username=username).first()
            if user and hasattr(user, 'profile'):
                profile = user.profile
                if not profile.is_locked():
                    profile.register_failed_attempt()
            raise serializers.ValidationError({'detail': 'No active account found with the given credentials'})

        # Password is correct, now let SimpleJWT continue
        self.user = user
        data = super().validate(attrs)

        # Reset login attempts
        if hasattr(user, 'profile'):
            user.profile.reset_login_attempts()
            data['encryption_salt'] = user.profile.encryption_salt

        data.pop('refresh', None)
        return data
