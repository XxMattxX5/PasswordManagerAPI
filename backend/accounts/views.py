from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from .forms import UserRegistrationForm

from django.contrib.auth.models import User

# Create your views here.
def home(request):
    return HttpResponse("Ok")

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CheckAuthentication(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(status=status.HTTP_200_OK)
    
class RegisterUser(APIView):

    def post(self, request):
        if (request.user.is_authenticated):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        form = UserRegistrationForm(request.data)

        if form.is_valid():
            
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            
            # User.objects.create_user(username, email, password)

            return Response({"message": "Account Created!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

        

