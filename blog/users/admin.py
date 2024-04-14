from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    # Fieldsets and other configurations if needed
    pass


# Re-register UserAdmin
admin.site.register(User, UserAdmin)
