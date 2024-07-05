from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from task_manager.forms import (CustomUserCreationForm,
                                LoginForm, StatusForm, TaskForm, LabelForm)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from task_manager.models import CustomUser, Status, Task, Label
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import logging
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.db.models import Q

logger = logging.getLogger(__name__)


def index(request):
    return HttpResponse("Hello, world. You're at the pollapp index.")


class IndexView(TemplateView):
    template_name = "index.html"
    extra_context = {'header': _('Task manager')}


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            messages.success(request, 'Пользователь успешно зарегистрирован')
            user.is_active = True
            user.save()
            # Удалите следующие строки, чтобы предотвратить автоматический вход пользователя
            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password1')
            # user = authenticate(request, username=username, password=password)
            # if user is not None:
            #     login(request, user)
            return redirect('login')  # Перенаправление на страницу входа
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})



def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'users/users.html', {'users': users})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы залогинены')
                return redirect('root')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль')
                return render(request, 'users/login.html', {'form': form})
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
            return render(request, 'users/login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, gettext_lazy('Вы разлогинены'))
    next_page = reverse_lazy('root')  # Указать желаемый URL вместо 'root'
    return redirect(next_page)


@login_required
def user_update_view(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    form = CustomUserCreationForm(instance=user)

    if user != request.user:
        messages.error(request,
                       'У вас нет прав для изменения другого пользователя.')
        return redirect('user-list')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно изменен')
            return redirect('user-list')

    return render(request, 'users/user_update.html', {'form': form})


@login_required
def user_delete_view(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)

    if user != request.user:
        messages.error(request,
                       'У вас нет прав для изменения другого пользователя.')
        return redirect('user-list')

    if request.method == 'GET':
        return render(request, 'users/user_delete.html', {'user': user})

    if request.method == 'POST':
        if user.author_tasks.exists() or user.executor_tasks.exists():
            messages.error(request,
                           'Невозможно удалить пользователя,'
                           ' потому что он используется')
            return redirect('user-list')
        else:
            user.delete()
            logout(request)
            messages.success(request, 'Пользователь успешно удален.')
            return HttpResponseRedirect(reverse('user-list'))

    return redirect('user-list')


@login_required(login_url='/require_login/')
def list_statuses(request):
    statuses = Status.objects.all()
    return render(request, 'statuses/statuses.html', {'statuses': statuses})


def require_login(request):
    messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
    return redirect('login')


@login_required
def create_status(request):
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статус успешно создан')
            return redirect('list_statuses')
    else:
        form = StatusForm()
    return render(request, 'statuses/create_status.html', {'form': form})


@login_required
def update_status(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статус успешно изменен')
            return redirect('list_statuses')
    else:
        form = StatusForm(instance=status)
    return render(request,
                  'statuses/update_status.html',
                  {'form': form, 'status': status})


@login_required
def delete_status(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        if status.tasks.exists():
            messages.error(request,
                           'Невозможно удалить статус,'
                           ' потому что он используется')
            return redirect('list_statuses')
        else:
            status.delete()
            messages.success(request, 'Статус успешно удален')
            return redirect('list_statuses')
    else:
        # Перенаправление на страницу подтверждения удаления
        return render(request,
                      'statuses/delete_status.html',
                      {'status': status})


def task_list(request):
    tasks = Task.objects.select_related('status', 'executor').prefetch_related('label').all()
    statuses = Status.objects.all()
    executors = CustomUser.objects.filter(executor_tasks__isnull=False).distinct()
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
        logger.info('Received POST request with data: %s', request.POST)
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
        messages.error(request, 'Задачу может удалить только ее автор')
        return redirect('task_list')

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Задача успешно удалена')
        return redirect('task_list')

    return render(request, 'tasks/task_delete.html', {'task': task})


@login_required
def label_create(request):
    if request.method == 'POST':
        form = LabelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Метка успешно создана.')
            return redirect('labels-list')
    else:
        form = LabelForm()
    return render(request, 'labels/label_create.html', {'form': form})


def label_delete(request, pk):
    label = get_object_or_404(Label, pk=pk)
    if request.method == 'POST':
        if label.label.exists():
            messages.error(request,
                           'Эту метку нельзя удалить,'
                           ' так как она связана с задачей.')
            return redirect('labels-list')
        else:
            label.delete()
            messages.success(request, 'Метка успешно удалена.')
            return redirect('labels-list')
    else:
        return render(request, 'labels/label_delete.html', {'label': label})


def label_update(request, pk):
    label = get_object_or_404(Label, pk=pk)
    if request.method == 'POST':
        form = LabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            messages.success(request, 'Метка успешно изменена')
            return redirect('labels-list')
        else:
            messages.error(request, 'Ошибка при обновлении метки.')
    else:
        form = LabelForm(instance=label)
    return render(request,
                  'labels/label_update.html',
                  {'form': form, 'label': label})


def labels_list(request):
    labels = Label.objects.all()
    return render(request, 'labels/labels.html', {'labels': labels})
