from django.contrib import admin
from .models import Assignment


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date', 'max_score', 'is_active', 'created_by', 'status_badge')  # Columns to display
    search_fields = ('title', 'course__name')  # Searchable fields (including course name)
    list_filter = ('course', 'due_date', 'is_active')  # Filters for the assignments

    def save_model(self, request, obj, form, change):
        # Automatically set the 'created_by' to the current user if not provided
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)