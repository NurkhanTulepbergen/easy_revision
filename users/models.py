from django.contrib.auth.models import AbstractUser
from django.db import models

# Пользователь с ролями
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('store', 'Store'),
        ('company', 'Company'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='store')
