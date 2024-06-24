from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


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
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=1)
    author = models.ForeignKey(CustomUser, related_name='author_tasks', on_delete=models.CASCADE)
    executor = models.ForeignKey(CustomUser, related_name='executor_tasks', on_delete=models.CASCADE, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
