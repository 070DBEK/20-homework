from django.db import models


class User(models.Model):
    ROLE_CHOICES = [
        ('teacher', 'Преподаватель'),
        ('student', 'Студент'),
        ('admin', 'Администратор'),
    ]

    full_name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name


