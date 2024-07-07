from django import forms
from .models import Status


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        labels = {
            'name': 'Имя',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                                    'placeholder': 'Имя'})
        }

    def __init__(self, *args, **kwargs):
        super(StatusForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.name:
            self.fields['name'].widget.attrs['placeholder']\
                = self.instance.name
