from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError, PermissionDenied


# Create your views here.
def home(request):
    return HttpResponse("Ok")

class CustomTokenView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = CustomTokenObtainPairSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_401_UNAUTHORIZED)
        except PermissionDenied as e:
            return Response(e.detail, status=status.HTTP_403_FORBIDDEN)


        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class CheckAuthentication(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Returns 200 if user is authenticated and 401 if not
        """
        return Response(status=status.HTTP_200_OK)
    
class RegisterUser(APIView):

    def post(self, request):
        """
        Handle user registration via POST request.

        - Returns 401 Unauthorized if the user is already authenticated.
        - Validates incoming user registration data using a Django form.
        - Creates a new user account if the form is valid.
        - Returns a 201 Created response with a success message on successful registration.
        - Returns form errors with a 400 Bad Request status if validation fails.

        """

        # Ensure user isn't authenticated
        if (request.user.is_authenticated):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        form = UserRegistrationForm(request.data)
        
        # Creates new user if form is valid
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            
            User.objects.create_user(username, email, password)

            return Response({"message": "Account Created!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

        

