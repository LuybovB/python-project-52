from django.contrib.auth.models import AbstractUser
from django.db import models
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
    name = models.CharField(
        verbose_name=_('Name'), max_length=100, validators=[])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))
    status = models.ForeignKey(Status,
                               on_delete=models.CASCADE,
                               related_name='tasks',
                               default=1,
                               verbose_name=_('Status'))
    author = models.ForeignKey(CustomUser,
                               related_name='author_tasks',
                               on_delete=models.CASCADE,
                               verbose_name=_('Author'))
    executor = models.ForeignKey(CustomUser,
                                 related_name='executor_tasks',
                                 on_delete=models.CASCADE,
                                 null=True,
                                 verbose_name=_('Executor'))
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Дата создания'))
    label = models.ManyToManyField(Label, related_name='label')

    def __str__(self):
        return self.name
