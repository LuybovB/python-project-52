from task_manager.labels.forms import LabelForm
from django.shortcuts import render, redirect, get_object_or_404
from task_manager.labels.models import Label
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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
    return render(request,
                  'labels/label_create.html', {'form': form})


def label_delete(request, pk):
    label = get_object_or_404(Label, pk=pk)
    if request.method == 'POST':
        if label.label.exists():
            messages.error(request,
                           'Невозможно удалить метку,'
                           ' потому что она используется')
            return redirect('labels-list')
        else:
            label.delete()
            messages.success(request, 'Метка успешно удалена.')
            return redirect('labels-list')
    else:
        return render(request, 'labels/label_delete.html',
                      {'label': label})


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
    return render(request, 'labels/labels.html',
                  {'labels': labels})
