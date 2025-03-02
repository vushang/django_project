from django.contrib import admin  # Импортируем модуль админки Django
from .models import UserDetail  # Импортируем модель UserDetail, которую будем регистрировать в админке

# Регистрируем модель UserDetail в админке с кастомными настройками
@admin.register(UserDetail)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Кастомное отображение модели UserDetail в админке Django.
    """
    list_display = ['user', 'title', 'description']  # Поля, отображаемые в списке объектов
    search_fields = ['user__username', 'title', 'description']  # Поля, по которым можно искать в админке
