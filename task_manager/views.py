from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from task_manager.forms import CustomUserCreationForm, LoginForm, StatusForm, TaskForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from task_manager.models import CustomUser, Status, Task
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')  # Используйте 'password1' из формы
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('root')  # Убедитесь, что 'root' существует в urls.py
            else:
                return redirect('login')
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
                messages.success(request, 'Вы загологинены')
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
    messages.success(request, 'Вы Разлогинены')
    return redirect('root')  # Указать желаемый URL вместо 'root'


@login_required
def user_update_view(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    form = CustomUserCreationForm(instance=user)

    if user != request.user:
        messages.error(request, 'У вас нет прав для изменения другого пользователя.')
        return redirect('user-list')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно обновлен.')
            return redirect('user-list')

    return render(request, 'users/user_update.html', {'form': form})


@login_required
def user_delete_view(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)

    if user != request.user:
        messages.error(request, 'У вас нет прав для удаления другого пользователя.')
        return redirect('user-list')

    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Пользователь успешно удален.')
        return HttpResponseRedirect(reverse('login'))

    return render(request, 'users/user_delete.html', {'user': user})


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
    return render(request, 'statuses/update_status.html', {'form': form, 'status': status})


@login_required
def delete_status(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if status.tasks.exists():
        messages.error(request, 'Невозможно удалить статус, потому что он используется')
        return HttpResponseForbidden('Статус связан с задачей и не может быть удален')
    if request.method == 'POST':
        status.delete()
        messages.success(request, 'Статус успешно удален')
        return redirect('list_statuses')
    return render(request, 'statuses/delete_status.html', {'status': status})


@login_required
def task_list(request):
    tasks = Task.objects.all()
    statuses = Status.objects.all()
    return render(request, 'tasks/tasks.html', {'tasks': tasks, 'statuses': statuses})


@login_required
def task_create(request):
    form = TaskForm(request.POST or None)
    if form.is_valid():
        task = form.save(commit=False)
        task.author = request.user
        # Добавьте следующую строку для установки статуса задачи
        task.status = form.cleaned_data.get('status')
        task.save()
        return redirect('task_list')
    else:
        statuses = Status.objects.all()  # Получаем все статусы из базы данных
        users = CustomUser.objects.all()
        return render(request, 'tasks/task_form.html', {'form': form, 'statuses': statuses, 'users': users})



@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)  # Сначала получаем задачу
    statuses = Status.objects.all()  # Получаем все статусы из базы данных
    users = CustomUser.objects.all()  # Получаем всех пользователей

    if request.user != task.author:
        return redirect('task_list')  # Проверяем, является ли пользователь автором

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)  # Создаем форму с данными POST и экземпляром задачи
        if form.is_valid():
            form.save()  # Сохраняем форму, если она валидна
            return redirect('task_list')  # Перенаправляем на список задач
    else:
        form = TaskForm(instance=task)  # Создаем пустую форму с экземпляром задачи для GET-запроса

    return render(request, 'tasks/task_form.html', {'form': form, 'statuses': statuses, 'users': users})



@login_required
def task_detail(request, pk):
    task = Task.objects.get(pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_delete(request, pk):
    task = Task.objects.get(pk=pk)
    if request.user == task.author:
        task.delete()
    return redirect('task_list')


def get_statuses(request):
    # Получаем все статусы из базы данных
    statuses = Status.objects.all().values('id', 'name')  # Пример полей: id и name
    status_list = list(statuses)  # Преобразуем QuerySet в список словарей
    return JsonResponse({'statuses': status_list})


def get_users(request):
    # Получаем всех пользователей из базы данных
    users = CustomUser.objects.all().values('id', 'username')  # Пример полей: id и username
    user_list = list(users)  # Преобразуем QuerySet в список словарей
    return JsonResponse({'users': user_list})