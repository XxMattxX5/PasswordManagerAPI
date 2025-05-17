from django.urls import path
from . import views



urlpatterns = [
    path("list/", views.PasswordList.as_view(), name="password-list"),
    path("folder/", views.Folders.as_view(), name="folder"),
    path("password/", views.Passwords.as_view(), name="password")
    
]