from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Password, PasswordFolder
from .serializers import UserPasswordListSerializer
from django.db.models import Prefetch


# Create your views here.

class PasswordList(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        user = request.user
        query = request.GET.get("q", "").strip()

        if query:
            folders = PasswordFolder.objects.filter(
                user=user,
                passwords__name__icontains=query
            ).prefetch_related(
                Prefetch(
                    'passwords',
                    queryset=Password.objects.filter(name__icontains=query)
                )
            ).distinct()
            
            unfoldered_passwords = Password.objects.filter(
                user=user,
                folder__isnull=True,
                name__icontains=query
            )
        else:
            folders = PasswordFolder.objects.filter(user=user).prefetch_related('passwords')
            unfoldered_passwords = Password.objects.filter(user=user, folder__isnull=True)
        
        data = {
            "folders": folders,
            "passwords": unfoldered_passwords,
        }
        
        serializer = UserPasswordListSerializer(data)
        return Response(serializer.data)

