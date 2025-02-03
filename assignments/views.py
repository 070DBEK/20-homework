from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Assignment
from .forms import AssignmentForm



class AssignmentListView(View):
    def get(self, request):
        assignments = Assignment.objects.all()
        return render(request, 'assignments/assignments.html', {'assignments': assignments})



class AssignmentDetailView(View):
    def get(self, request, pk):
        assignment = get_object_or_404(Assignment, pk=pk)
        return render(request, 'assignments/assignments-detail.html', {'assignment': assignment})



class AssignmentCreateView(View):
    def get(self, request):
        form = AssignmentForm()
        return render(request, 'assignments/assignments-form.html', {'form': form})

    def post(self, request):
        form = AssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Задание успешно создано.")
            return redirect('assignments:list')
        return render(request, 'assignments/assignments-form.html', {'form': form})


class AssignmentUpdateView(View):
    def get(self, request, pk):
        assignment = get_object_or_404(Assignment, pk=pk)
        form = AssignmentForm(instance=assignment)
        return render(request, 'assignments/assignments-form.html', {'form': form})

    def post(self, request, pk):
        assignment = get_object_or_404(Assignment, pk=pk)
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, "Задание успешно обновлено.")
            return redirect('assignments:list')
        return render(request, 'assignments/assignments-form.html', {'form': form})


class AssignmentDeleteView(View):
    def get(self, request, pk):
        assignment = get_object_or_404(Assignment, pk=pk)
        return render(request, 'assignments/assignments-delete-confirm.html', {'assignment': assignment})

    def post(self, request, pk):
        assignment = get_object_or_404(Assignment, pk=pk)
        assignment.delete()
        messages.success(request, "Задание успешно удалено.")
        return redirect('assignments:list')