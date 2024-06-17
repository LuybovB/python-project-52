from django import forms
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    first_name = forms.CharField(
        label=_('Имя'),
        min_length=3,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Имя')})
    )
    last_name = forms.CharField(
        label=_('Фамилия'),
        min_length=3,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Фамилия')})
    )
    username = forms.CharField(
        label=_('Имя пользователя'),
        max_length=150,
        help_text=_('Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Имя пользователя')})
    )
    password = forms.CharField(
        label=_('Пароль'),
        help_text=_('• Ваш пароль должен содержать как минимум 3 символа.'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Пароль')}))

    password2 = forms.CharField(
        label=_('Подтверждение пароля'),
        help_text=_('Для подтверждения введите, пожалуйста, пароль ещё раз.'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Подтверждение пароля')}))

    class Meta:
        model = CustomUser  # Укажите здесь вашу модель пользователя
        fields = ('first_name', 'last_name', 'username', 'password', 'password2')



    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = '<span style="font-size: smaller;">{}</span>'.format(self.fields['username'].help_text)
        self.fields['password'].help_text = '<span style="font-size: smaller;">{}</span>'.format(self.fields['password'].help_text)
        self.fields['password2'].help_text = '<span style="font-size: smaller;">{}</span>'.format(self.fields['password2'].help_text)



    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError(_('Пароли не совпадают'))
        return password2


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())
