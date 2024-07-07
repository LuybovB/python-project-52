from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from task_manager.forms import (CustomUserCreationForm,
                                LoginForm)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from task_manager.models import CustomUser
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import logging
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy

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
    next_page = reverse_lazy('root')
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
