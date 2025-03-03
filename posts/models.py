from ckeditor.fields import RichTextField  # Поле с расширенным редактором текста
from django.conf import settings  # Импортируем настройки Django (используется для указания модели пользователя)
from django.db import models  # Импортируем модуль моделей Django


# Модель категории постов
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название категории')  
    slug = models.SlugField(unique=True, help_text='Рекомендуется не изменять это вручную.')  

    def __str__(self):
        return self.name  


# Модель тегов для постов
class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название тега')  
    slug = models.SlugField(unique=True, help_text='Рекомендуется не изменять это вручную.')  

    def __str__(self):
        return self.name 


# Модель для подсчета просмотров
class HitCount(models.Model):
    ip = models.CharField(max_length=100)  # Сохраняет IP-адрес пользователей

    def __str__(self):
        return self.ip  


# Модель постов
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Теги')  
    views = models.ManyToManyField(HitCount, related_name='post_views', blank=True)  
    title = models.CharField(max_length=75, verbose_name='Заголовок')  
    slug = models.SlugField(unique=True, help_text='Рекомендуется не изменять это вручную.')  
    image = models.ImageField(upload_to='posts/%Y/%m/%d/', verbose_name='Изображение')  
    content = RichTextField(verbose_name='Контент')  
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')  
    available = models.BooleanField(default=True, verbose_name='Активный/Неактивный')  

    def __str__(self):
        return self.title  

    def getHitCount(self):
        """Возвращает количество просмотров поста"""
        return self.views.count()

    class Meta:
        ordering = ['-created']  


# Модель комментариев к постам
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)  
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    content = models.TextField(verbose_name='Комментарий')  
    created = models.DateTimeField(auto_now_add=True)  
    available = models.BooleanField(default=True, verbose_name='Активный/Неактивный')  

    class Meta:
        ordering = ['-created']  

    def __str__(self):
        return self.author.username + ' | ' + self.post.title  
