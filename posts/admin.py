from django.contrib import admin  

from .models import Category, Tag, HitCount, Post, Comment 


# Регистрация модели Category в админке
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}  
    list_display = ['name', 'slug']  
    search_fields = ['name'] 


# Регистрация модели Tag в админке
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}  
    list_display = ['name', 'slug']  
    search_fields = ['name']  


# Регистрация модели HitCount в админке
@admin.register(HitCount)
class HitCountAdmin(admin.ModelAdmin):
    list_display = ['ip']  
    search_fields = ['ip']  


# Регистрация модели Post в админке
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}  
    list_display = ['title', 'created', 'category', 'available', 'getHitCount'] 
    list_display_links = ['title', 'created'] 
    list_filter = ['created', 'category', 'tags']  
    search_fields = ['title', 'content']  


# Регистрация модели Comment в админке
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created', 'available']  
    list_display_links = ['post', 'author']  
    list_filter = ['post', 'author', 'created', 'available']  
    search_fields = ['post__title', 'author__username', 'content']  