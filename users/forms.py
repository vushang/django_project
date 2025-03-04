from django import forms  
from .models import UserDetail  
from django.contrib.auth.models import User  


class UserForm(forms.ModelForm):
    """
    Форма для редактирования данных пользователя (модель User).
    Добавляет стили для полей ввода.
    """
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))  
    
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))  
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    })) 
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
    }))  

    class Meta:
        model = User  
        fields = ['first_name', 'last_name', 'username', 'email']  


class UserDetailForm(forms.ModelForm):
    """
    Форма для редактирования дополнительных данных пользователя (модель UserDetail).
    Позволяет изменять заголовок, описание и изображение.
    """
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))  
    
    description = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))  
    
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'form-control'
    }))  

    class Meta:
        model = UserDetail  
        fields = ['title', 'description', 'image']  
