from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Course(BaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название курса")
    code = models.CharField(max_length=50, unique=True, verbose_name="Код курса")
    description = models.TextField(blank=True, verbose_name="Описание")
    instructor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='courses', verbose_name="Преподаватель"
    )
    start_date = models.DateField(verbose_name="Дата начала")
    duration = models.PositiveIntegerField(
        verbose_name="Продолжительность (недель)",
        validators=[MinValueValidator(1), MaxValueValidator(52)]
    )

    class Meta:
        verbose_name_plural = "Курсы"
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.name} ({self.code})"
