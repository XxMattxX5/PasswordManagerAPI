from django.contrib import admin
from .models import PasswordFolder, Password

class PasswordInline(admin.TabularInline):
    model = Password
    extra = 0
    fields = ("user",'name', 'username', 'password', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(PasswordFolder)
class PasswordFolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'user','updated_at', 'created_at')
    inlines = [PasswordInline]

@admin.register(Password)
class PasswordAdmin(admin.ModelAdmin):
    list_display = ('name', 'folder', 'username', 'created_at', 'updated_at')
    search_fields = ('name', 'username', 'folder__name')
