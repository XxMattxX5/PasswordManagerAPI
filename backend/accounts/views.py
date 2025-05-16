from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated

# Create your views here.
def home(request):
    return HttpResponse("Ok")

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CheckAuthentication(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(status=status.HTTP_200_OK)
        

