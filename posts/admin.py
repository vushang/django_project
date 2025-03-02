from django.contrib import admin  # Импортируем модуль админки Django

from .models import Category, Tag, HitCount, Post, Comment  # Импортируем модели


# Регистрация модели Category в админке
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}  # Автоматическое заполнение slug на основе name
    list_display = ['name', 'slug']  # Отображаемые поля в списке объектов
    search_fields = ['name']  # Поле, по которому можно искать в админке


# Регистрация модели Tag в админке
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}  # Автоматическое заполнение slug на основе name
    list_display = ['name', 'slug']  # Отображаемые поля в списке объектов
    search_fields = ['name']  # Поле, по которому можно искать в админке


# Регистрация модели HitCount в админке
@admin.register(HitCount)
class HitCountAdmin(admin.ModelAdmin):
    list_display = ['ip']  # Отображаемые поля в списке объектов
    search_fields = ['ip']  # Поле, по которому можно искать в админке


# Регистрация модели Post в админке
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}  # Автоматическое заполнение slug на основе title
    list_display = ['title', 'created', 'category', 'available', 'getHitCount']  # Поля в списке объектов
    list_display_links = ['title', 'created']  # Поля, которые можно кликать для перехода в объект
    list_filter = ['created', 'category', 'tags']  # Фильтры в админке
    search_fields = ['title', 'content']  # Поля для поиска (исправлено поле description на content)


# Регистрация модели Comment в админке
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created', 'available']  # Поля в списке объектов
    list_display_links = ['post', 'author']  # Поля, которые можно кликать
    list_filter = ['post', 'author', 'created', 'available']  # Фильтры
    search_fields = ['post__title', 'author__username', 'content']  # Поля для поиска (исправлены ошибки)
