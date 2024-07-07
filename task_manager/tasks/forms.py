from django import forms
from .models import Task
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.models import CustomUser


class TaskForm(forms.ModelForm):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    executor = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Описание',
            'rows': 10,
            'required': False
        }),
        required=False
    )

    label = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        widget=forms.SelectMultiple,
        required=False
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'label']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название задания',
                'required': 'required',
                'oninvalid': "this.setCustomValidity("
                             "'Пожалуйста, заполните это поле')",
                'oninput': "setCustomValidity('')"
            })
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False
