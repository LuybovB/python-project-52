from django.db import models
from django.utils.translation import gettext_lazy as _
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.models import CustomUser


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
