from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Course
from assignments.models import Assignment
from users.models import User
from .forms import CourseForm
from datetime import date


def home(request):
    # Fetch data for active courses, assignments, and users
    active_courses = Course.objects.count()
    active_assignments = Assignment.objects.count()
    registered_users = User.objects.count()

    # Pass the data to the template
    context = {
        'active_courses': active_courses,
        'active_assignments': active_assignments,
        'registered_users': registered_users,
    }

    return render(request, 'index.html', context)

class CourseListView(View):
    """Kurslar ro‘yxatini chiqarish"""

    def get(self, request):
        courses = Course.objects.all()
        return render(request, "courses/courses.html", {"courses": courses})


class CourseCreateView(View):
    def get(self, request):
        form = CourseForm()
        return render(request, "courses/course-form.html", {
            "form": form,
            "today": date.today()
        })

    def post(self, request):
        if not request.user.is_authenticated or request.user.role not in ['teacher', 'admin']:
            return HttpResponseForbidden("Sizga ruxsat yo‘q")

        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, "Курс успешно создан!")
            return redirect("course_list")

        return render(request, "courses/course-form.html", {"form": form})



class CourseUpdateView(View):
    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        # Admin ham tahrirlay oladi
        if request.user.role != 'admin' and request.user != course.instructor:
            return HttpResponseForbidden("Siz faqat o‘z kurslaringizni tahrirlashingiz mumkin")

        form = CourseForm(instance=course)
        return render(request, "courses/course-form.html", {"form": form})

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        if request.user != course.instructor and request.user.role != 'admin':
            return HttpResponseForbidden("Siz faqat o‘z kurslaringizni tahrirlashingiz mumkin")

        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Курс успешно обновлен!")
            return redirect("course_list")

        return render(request, "courses/course-form.html", {"form": form})


class CourseDeleteView(View):
    """Kursni o‘chirish"""

    def get(self, request, pk):
        """O‘chirishni tasdiqlash sahifasini ko‘rsatish"""
        course = get_object_or_404(Course, pk=pk)
        if request.user != course.instructor and request.user.role != 'admin':
            return HttpResponseForbidden("Siz faqat o‘z kurslaringizni o‘chirishingiz mumkin")

        return render(request, "courses/course-delete-confirm.html", {"course": course})

    def post(self, request, pk):
        """Tasdiqlangandan keyin kursni o‘chirish"""
        course = get_object_or_404(Course, pk=pk)
        if request.user != course.instructor and request.user.role != 'admin':
            return HttpResponseForbidden("Siz faqat o‘z kurslaringizni o‘chirishingiz mumkin")

        course.delete()
        messages.success(request, "Курс успешно удален!")
        return redirect("courses:list")
