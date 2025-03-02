from django import forms  # Импортируем модуль forms для создания форм Django
from .models import UserDetail  # Импортируем модель UserDetail, которая хранит доп. информацию о пользователе
from django.contrib.auth.models import User  # Импортируем встроенную модель User


class UserForm(forms.ModelForm):
    """
    Форма для редактирования данных пользователя (модель User).
    Добавляет стили для полей ввода.
    """
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))  # Поле для имени пользователя с кастомным стилем
    
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))  # Поле для фамилии пользователя
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))  # Поле для имени пользователя (логина)
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
    }))  # Поле для email пользователя

    class Meta:
        model = User  # Указываем, что форма связана с моделью User
        fields = ['first_name', 'last_name', 'username', 'email']  # Список полей, которые будут в форме


class UserDetailForm(forms.ModelForm):
    """
    Форма для редактирования дополнительных данных пользователя (модель UserDetail).
    Позволяет изменять заголовок, описание и изображение.
    """
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))  # Поле для заголовка профиля
    
    description = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))  # Поле для описания профиля
    
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'form-control'
    }))  # Поле для загрузки изображения

    class Meta:
        model = UserDetail  # Указываем, что форма связана с моделью UserDetail
        fields = ['title', 'description', 'image']  # Список полей, которые будут в форме
