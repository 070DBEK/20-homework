from django.contrib import admin
from  .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'instructor', 'start_date', 'duration')  # Columns to display
    search_fields = ('name', 'code')  # Searchable fields
    list_filter = ('instructor', 'start_date')  # Filter courses by instructor or start date

    def save_model(self, request, obj, form, change):
        # Set the instructor to the current user automatically if not provided
        if not obj.instructor:
            obj.instructor = request.user
        super().save_model(request, obj, form, change)