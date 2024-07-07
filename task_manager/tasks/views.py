from task_manager.tasks.forms import TaskForm
from django.shortcuts import render, redirect, get_object_or_404
from task_manager.models import CustomUser
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)


def task_list(request):
    tasks = Task.objects.select_related(''
                                        'status',
                                        'executor'
                                        ).prefetch_related(
        'label').all()
    statuses = Status.objects.all()
    executors = CustomUser.objects.filter(
        executor_tasks__isnull=False).distinct()
    labels = Label.objects.all()

    status_id = request.GET.get('status')
    if status_id:
        tasks = tasks.filter(status_id=status_id)

    executor_id = request.GET.get('executor')
    if executor_id:
        tasks = tasks.filter(executor_id=executor_id)

    label_id = request.GET.get('label')
    if label_id:
        tasks = tasks.filter(label__id=label_id)

    if 'own_tasks' in request.GET:
        tasks = tasks.filter(author=request.user)

    logger.debug('Filtered tasks: %s', list(tasks.values('id', 'name')))
    logger.debug('Filtered status ID: %s', status_id)
    logger.debug('Filtered executor ID: %s', executor_id)
    logger.debug('Filtered label ID: %s', label_id)

    return render(request, 'tasks/tasks.html', {
        'tasks': tasks,
        'statuses': statuses,
        'executors': executors,
        'labels': labels,
    })


@login_required
def task_create(request):
    form = TaskForm(request.POST or None)
    labels = Label.objects.all()
    if request.method == 'POST':
        logger.info('Received POST request with data: %s',
                    request.POST)
        if form.is_valid():
            logger.info('Form is valid')
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            task.label.set(request.POST.getlist('label'))
            messages.success(request, 'Задача успешно создана')
            return redirect('task_list')
        else:
            logger.warning('Form is not valid: %s', form.errors)
    statuses = Status.objects.all()
    users = CustomUser.objects.all()
    return render(request, 'tasks/task_form.html', {
        'form': form,
        'statuses': statuses,
        'users': users,
        'labels': labels
    })


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    statuses = Status.objects.all()
    users = CustomUser.objects.all()
    labels = Label.objects.all()

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задача успешно изменена')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/task_update.html', {
        'form': form,
        'statuses': statuses,
        'users': users,
        'labels': labels,
        'task': task
    })


@login_required
def task_detail(request, pk):
    task = Task.objects.get(pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.user != task.author:
        messages.error(request,
                       'Задачу может удалить только ее автор')
        return redirect('task_list')

    if request.method == 'POST':
        task.delete()
        messages.success(request,
                         'Задача успешно удалена')
        return redirect('task_list')

    return render(request, 'tasks/task_delete.html', {'task': task})
