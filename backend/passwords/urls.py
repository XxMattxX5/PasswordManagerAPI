from django.urls import path
from . import views



urlpatterns = [
    path("list/", views.PasswordList.as_view(), name="password-list")
    
]