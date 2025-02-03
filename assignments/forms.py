from django import forms
from .models import Assignment
from datetime import date


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'course', 'description', 'due_date', 'max_score', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': 'Введите название задания'
            }),
            'course': forms.Select(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
            }),
            'description': forms.Textarea(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': 'Введите описание задания',
                'rows': 4
            }),
            'due_date': forms.DateTimeInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'type': 'datetime-local'
            }),
            'max_score': forms.NumberInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'min': 1,
                'step': 1
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-5 w-5 text-blue-600'
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title or len(title) > 255:
            raise forms.ValidationError("Название задания должно быть заполнено и не превышать 255 символов.")
        return title

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date.date() < date.today():
            raise forms.ValidationError("Срок сдачи должен быть в будущем.")
        return due_date

    def clean_max_score(self):
        max_score = self.cleaned_data.get('max_score')
        if max_score is not None and max_score <= 0:
            raise forms.ValidationError("Максимальный балл должен быть больше 0.")
        return max_score
