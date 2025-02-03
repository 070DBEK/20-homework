from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Course
from users.models import User


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'description', 'instructor', 'start_date', 'duration']
        widgets = {
            'name': forms.TextInput(attrs={
                "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                "placeholder": "Введите название курса"
            }),
            'code': forms.TextInput(attrs={
                "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                "placeholder": "Введите код курса"
            }),
            'description': forms.Textarea(attrs={
                "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                "placeholder": "Введите описание курса",
                "rows": 4
            }),
            'start_date': forms.DateInput(attrs={
                "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                "type": "date"
            }),
            'duration': forms.NumberInput(attrs={
                "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                "min": 1,
                "max": 52,
                "placeholder": "Введите продолжительность (в неделях)"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['instructor'].queryset = User.objects.filter(role='teacher')

    def clean_instructor(self):
        instructor = self.cleaned_data.get('instructor')
        if instructor and instructor.role != 'teacher':
            raise ValidationError("Только преподаватели могут быть инструкторами курса")
        return instructor

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not code.isalnum() or ' ' in code:
            raise ValidationError("Код курса должен содержать только буквы и цифры без пробелов")

        # Kursni tahrirlashda avvalgi kodni tekshirish
        if Course.objects.exclude(pk=self.instance.pk).filter(code=code).exists():
            raise ValidationError("Курс с таким кодом уже существует!")
        return code

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date and start_date < timezone.localdate():
            raise ValidationError("Дата начала не может быть в прошлом")
        return start_date
