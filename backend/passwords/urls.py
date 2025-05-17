from django.urls import path
from . import views



urlpatterns = [
    path("list/", views.PasswordList.as_view(), name="password-list"),
    path("folder/create/", views.CreateFolder.as_view(), name="create-folder"),
    path("folder/<int:id>/", views.Folders.as_view(), name="folders"),
    path("create/", views.CreatePassword.as_view(), name="create-password"),
    path("<int:id>/", views.Passwords.as_view(), name="passwords"),
    
]