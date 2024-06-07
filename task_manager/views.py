from django.views.generic import TemplateView

from django.utils.translation import gettext_lazy as _
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect


class IndexView(TemplateView):
    template_name = "index.html"
    extra_context = {
        'header': _('Task manager'),
    }

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('root')  # Предполагается, что 'index' - это имя вашего URL для главной страницы
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})