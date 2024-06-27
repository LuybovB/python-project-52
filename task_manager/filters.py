from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import django_filters
from .models import Task, Status, CustomUser, Label


@login_required
def task_list(request):
    filter = TaskFilter(request.GET, queryset=Task.objects.all(),
                        request=request)
    return render(request, 'tasks/tasks.html', {'filter': filter})


class TaskFilter(django_filters.FilterSet):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TaskFilter, self).__init__(*args, **kwargs)

    status = django_filters.ModelChoiceFilter(queryset=Status.objects.all())
    executor = django_filters.ModelChoiceFilter(
        queryset=CustomUser.objects.all())
    label = django_filters.ModelChoiceFilter(queryset=Label.objects.all())
    is_author = django_filters.BooleanFilter(
        method='filter_is_author', label='Только свои задачи')

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label']

    def filter_is_author(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
