from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'password', 'first_name', 'last_name', 'is_staff', 'is_active')  # Поля, которые вы хотите отобразить
    list_filter = ('is_staff', 'is_active')  # Фильтры для удобного поиска
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        # Добавьте другие разделы и поля по мере необходимости
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')  # Поля поиска
    ordering = ('username',)  # Порядок сортировки

admin.site.register(CustomUser, CustomUserAdmin)
