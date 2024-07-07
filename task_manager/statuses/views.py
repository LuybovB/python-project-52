from task_manager.statuses.forms import StatusForm
from django.shortcuts import render, redirect, get_object_or_404
from task_manager.statuses.models import Status
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url='/require_login/')
def list_statuses(request):
    statuses = Status.objects.all()
    return render(request, 'statuses/statuses.html', {'statuses': statuses})


def require_login(request):
    messages.error(request,
                   'Вы не авторизованы! Пожалуйста, выполните вход.')
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
