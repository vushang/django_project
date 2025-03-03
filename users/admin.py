from django.contrib import admin 
from .models import UserDetail 


@admin.register(UserDetail)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Кастомное отображение модели UserDetail в админке Django.
    """
    list_display = ['user', 'title', 'description']  # Поля, отображаемые в списке объектов
    search_fields = ['user__username', 'title', 'description']  # Поля, по которым можно искать в админке
