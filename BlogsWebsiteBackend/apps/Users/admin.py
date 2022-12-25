from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class UserAdminConfig(UserAdmin):
    ordering = ('-created_at',)
    list_display = ('email', 'user_name', 'first_name', 'last_name', 'role', 'is_active', 'is_staff')
    fieldsets = (
        (None, {"fields": ('email', 'user_name', 'first_name', 'last_name')}),
        ("Permissions", {"fields": ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ("Roles", {"fields": ('role',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'last_name', 'role',
                       'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )
    list_editable = ('is_staff', 'is_active')
    