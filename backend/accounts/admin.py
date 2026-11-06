from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Study Buddy', {'fields': ('name', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Study Buddy', {'fields': ('name', 'email', 'role')}),
    )
    list_display = ('username', 'name', 'email', 'role', 'is_staff')
    list_filter = UserAdmin.list_filter + ('role',)