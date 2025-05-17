from rest_framework import serializers
from .models import Password, PasswordFolder

class PasswordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Password
        fields = ['id', 'name']

class PasswordFolderListSerializer(serializers.ModelSerializer):
    passwords = PasswordListSerializer(many=True) 

    class Meta:
        model = PasswordFolder
        fields = ['id', 'name', 'passwords']

class UserPasswordListSerializer(serializers.Serializer):
    folders = PasswordFolderListSerializer(many=True)
    passwords = PasswordListSerializer(many=True)


class PasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Password
        fields = ["id","name","username", "password"]
        read_only_fields = ["id"]

class FolderSerializer(serializers.ModelSerializer):

    class Meta:
        model = PasswordFolder
        fields = ["id", "name"]
        read_only_fields = ["id"]