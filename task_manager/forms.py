from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    first_name = forms.CharField(
        label=_('Имя'),
        min_length=3,
        max_length=50,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': _('Имя')})
    )
    last_name = forms.CharField(
        label=_('Фамилия'),
        min_length=3,
        max_length=50,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': _('Фамилия')})
    )
    username = forms.CharField(
        label=_('Имя пользователя'),
        max_length=150,
        help_text=_(
            'Обязательное поле. Не более 150 символов.'
            ' Только буквы, цифры и символы @/./+/-/_.'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Имя пользователя')
            })
    )
    password1 = forms.CharField(
        label=_('Пароль'),
        help_text=_(
            '• Ваш пароль должен содержать как минимум 3 символа.'),
        widget=forms.PasswordInput(  # Используйте PasswordInput здесь
            attrs={'class': 'form-control', 'placeholder': _('Пароль')})
    )

    password2 = forms.CharField(
        label=_('Подтверждение пароля'),
        help_text=_('Для подтверждения введите, пожалуйста, пароль ещё раз.'),
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': _('Подтверждение пароля')}))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'username')

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password1"]
        user.set_password(password)
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        label=_('Имя пользователя'),
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': _('Имя пользователя')})
    )
    password = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': _('Пароль')})
    )


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username')
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Имя'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Фамилия'}),
            'username': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Имя пользователя'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
