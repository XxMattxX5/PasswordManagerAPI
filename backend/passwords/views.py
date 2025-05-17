from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Password, PasswordFolder
from .serializers import UserPasswordListSerializer, PasswordSerializer, FolderSerializer
from django.db.models import Prefetch
from .forms import CreateFolderForm, CreatePasswordForm
from django.shortcuts import get_object_or_404


# Create your views here.
class PasswordList(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        """
        Retrieve a list of password folders and unfoldered passwords for the authenticated user.
        Supports optional filtering by a search query on password names.

        Query Params:
            q (str): Optional search string to filter passwords by name.

        Returns:
            Response: JSON response containing folders with matching passwords and
                      unfoldered passwords matching the query. Returns all if no query.
        """
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
    
class CreatePassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Create a new password entry for the authenticated user.
        Optionally associate the password with an existing folder.

        Request Body:
            accountName (str): Name of the account.
            username (str): Username for the account.
            password (str): Password for the account.
            folderId (int, optional): ID of the folder to associate the password with.

        Returns:
            Response: HTTP 200 OK on successful creation.
                      HTTP 403 Forbidden if the user does not own the specified folder.
                      HTTP 400 Bad Request if form validation fails.
        """
        form = CreatePasswordForm(request.data)

        if form.is_valid():
            user = request.user
            accountName = form.cleaned_data["accountName"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            
            folder_id = request.data.get('folderId')

            if folder_id:
                folder = get_object_or_404(PasswordFolder, id=folder_id)

                if (user != folder.user):
                    return Response({"message":"You do not own the selected folder"}, status=status.HTTP_403_FORBIDDEN)

                Password.objects.create(
                    user=user,
                    name=accountName,
                    username=username,
                    password=password,
                    folder=folder  
                )
            else:
                
                Password.objects.create(
                    user=user,
                    name=accountName,
                    username=username,
                    password=password
                )
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class Passwords(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request, id):
        """
        Retrieve details of a single password entry by ID for the authenticated user.

        Args:
            id (int): ID of the password to retrieve.

        Returns:
            Response: JSON response with password data if found and owned by user.
                      HTTP 403 Forbidden if the password does not belong to the user.
                      HTTP 404 Not Found if the password does not exist.
        """
        user = request.user
        password = get_object_or_404(Password, id=id)

        if (user != password.user):
            return Response({"message":"Password does not belong to user"}, status=status.HTTP_403_FORBIDDEN)
        
        data = PasswordSerializer(password).data

        return Response({"data":data}, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        """
        Update an existing password entry by ID for the authenticated user.

        Args:
            id (int): ID of the password to update.
        
        Request Body:
            Fields for the PasswordSerializer to update the password instance.

        Returns:
            Response: HTTP 200 OK if update is successful.
                      HTTP 403 Forbidden if the password does not belong to the user.
                      HTTP 400 Bad Request if validation fails.
                      HTTP 404 Not Found if the password does not exist.
        """
        user = request.user
        password = get_object_or_404(Password, id=id)

        if (user != password.user):
            return Response({"message":"Password does not belong to user"}, status=status.HTTP_403_FORBIDDEN)

        serializer = PasswordSerializer(password, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=400)
    
    def delete(self, request, id):
        """
        Delete a password entry by ID for the authenticated user.

        Args:
            id (int): ID of the password to delete.

        Returns:
            Response: HTTP 200 OK with success message on deletion.
                      HTTP 403 Forbidden if the password does not belong to the user.
                      HTTP 404 Not Found if the password does not exist.
        """
        user = request.user
        password = get_object_or_404(Password, id=id)

        if (user != password.user):
            return Response({"message":"Password does not belong to user"}, status=status.HTTP_403_FORBIDDEN)

        password.delete()

        return Response({"message": "Password deleted successfully"},status=status.HTTP_200_OK)
        

class CreateFolder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Create a new password folder for the authenticated user.

        Request Body:
            folderName (str): The name of the new folder to create.

        Returns:
            Response: HTTP 200 OK on successful creation.
                      HTTP 400 Bad Request if the form validation fails.
        """
        form = CreateFolderForm(request.data)

        if form.is_valid():
            user = request.user
            folderName = form.cleaned_data["folderName"]

            PasswordFolder.objects.create(name=folderName, user=user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
class Folders(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request, id):
        """
        Retrieve details of a specific password folder by ID for the authenticated user.

        Args:
            id (int): ID of the folder to retrieve.

        Returns:
            Response: JSON response with folder data if found and owned by user.
                      HTTP 403 Forbidden if the folder does not belong to the user.
                      HTTP 404 Not Found if the folder does not exist.
        """
        user = request.user
        folder = get_object_or_404(PasswordFolder, id=id)

        if (user != folder.user):
            return Response({"message":"Folder does not belong to user"}, status=status.HTTP_403_FORBIDDEN)
        
        data = FolderSerializer(folder).data

        return Response({"data":data}, status=status.HTTP_200_OK)

    def put(self,request, id):
        """
        Update a specific password folder by ID for the authenticated user.

        Args:
            id (int): ID of the folder to update.

        Request Body:
            Fields for the FolderSerializer to update the folder instance.

        Returns:
            Response: HTTP 200 OK if update is successful.
                      HTTP 403 Forbidden if the folder does not belong to the user.
                      HTTP 400 Bad Request if validation fails.
                      HTTP 404 Not Found if the folder does not exist.
        """
        user = request.user
        folder = get_object_or_404(PasswordFolder, id=id)

        if (user != folder.user):
            return Response({"message":"Folder does not belong to user"}, status=status.HTTP_403_FORBIDDEN)

        serializer = FolderSerializer(folder, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        """
        Delete a specific password folder by ID for the authenticated user.

        Args:
            id (int): ID of the folder to delete.

        Returns:
            Response: HTTP 200 OK with success message on deletion.
                      HTTP 403 Forbidden if the folder does not belong to the user.
                      HTTP 404 Not Found if the folder does not exist.
        """
        user = request.user
        folder = get_object_or_404(PasswordFolder, id=id)

        if (user != folder.user):
            return Response({"message":"Folder does not belong to user"}, status=status.HTTP_403_FORBIDDEN)

        folder.delete()

        return Response({"message": "Folder deleted successfully"},status=status.HTTP_200_OK)

