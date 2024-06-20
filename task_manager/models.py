from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=100)
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.username


class Status(models.Model):
    name = models.CharField(verbose_name=_('Имя'), max_length=100, validators=[])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    status = models.ForeignKey('Status', on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=100)
    description = models.TextField()

