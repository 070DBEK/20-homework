from django.db import models
from courses.models import Course, BaseModel
from django.contrib.auth import get_user_model


class Assignment(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Название задания")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    description = models.TextField(verbose_name="Описание")
    due_date = models.DateField(verbose_name="Срок сдачи")
    max_score = models.PositiveIntegerField(verbose_name="Максимальный балл")
    is_active = models.BooleanField(default=True, verbose_name="Активное")
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def status_badge(self):
        return "bg-green-100 text-green-800" if self.is_active else "bg-red-100 text-red-800"

    def __str__(self):
        return self.title
