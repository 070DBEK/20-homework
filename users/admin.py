from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'role', 'password')  # Columns to display in the list view
    search_fields = ('full_name', 'email')  # Fields to search by in the admin
    list_filter = ('role',)  # Filter users by their role

    def has_change_permission(self, request, obj=None):
        # Customizing the permission to disable editing the password field directly
        if obj and obj.role == 'admin':
            return False
        return super().has_change_permission(request, obj)