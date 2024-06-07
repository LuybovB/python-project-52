from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Имя')
    last_name = forms.CharField(max_length=30, required=True, help_text='Фамилия')
    username = forms.CharField(max_length=150, required=True, help_text='Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')
