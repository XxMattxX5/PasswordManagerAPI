from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Remove the refresh token from the response
        data.pop('refresh', None)

        # Add encryption_salt from user profile
        data['encryption_salt'] = self.user.profile.encryption_salt

        return data