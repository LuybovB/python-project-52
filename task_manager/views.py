from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserCreationForm, LoginForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



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
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('root')  # Указать желаемый URL вместо 'desired_page'
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
            print(f"Попытка входа для пользователя: {username}")  # Для отладки
            user = authenticate(request, username=username, password=password)
            print(f"Пользователь {'не ' if user is None else ''}аутентифицирован")  # Для отладки
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы загологинены')
                return redirect('root')
            else:
                form.add_error(None, 'Неверное имя пользователя или пароль')
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