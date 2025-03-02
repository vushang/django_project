from ckeditor.fields import RichTextField  # Поле с расширенным редактором текста
from django.conf import settings  # Импортируем настройки Django (используется для указания модели пользователя)
from django.db import models  # Импортируем модуль моделей Django


# Модель категории постов
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название категории')  # Название категории
    slug = models.SlugField(unique=True, help_text='Рекомендуется не изменять это вручную.')  # Уникальный slug

    def __str__(self):
        return self.name  # Возвращает название категории в строковом представлении


# Модель тегов для постов
class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название тега')  # Название тега
    slug = models.SlugField(unique=True, help_text='Рекомендуется не изменять это вручную.')  # Уникальный slug

    def __str__(self):
        return self.name  # Возвращает название тега в строковом представлении


# Модель для подсчета просмотров
class HitCount(models.Model):
    ip = models.CharField(max_length=100)  # Сохраняет IP-адрес пользователей

    def __str__(self):
        return self.ip  # Возвращает IP-адрес в строковом представлении


# Модель постов
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Автор поста
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Категория поста
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Теги')  # Теги поста
    views = models.ManyToManyField(HitCount, related_name='post_views', blank=True)  # Количество просмотров
    title = models.CharField(max_length=75, verbose_name='Заголовок')  # Заголовок поста
    slug = models.SlugField(unique=True, help_text='Рекомендуется не изменять это вручную.')  # Уникальный slug
    image = models.ImageField(upload_to='posts/%Y/%m/%d/', verbose_name='Изображение')  # Изображение к посту
    content = RichTextField(verbose_name='Контент')  # Контент поста с расширенным текстовым редактором
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')  # Дата создания поста
    available = models.BooleanField(default=True, verbose_name='Активный/Неактивный')  # Доступность поста

    def __str__(self):
        return self.title  # Возвращает заголовок поста в строковом представлении

    def getHitCount(self):
        """Возвращает количество просмотров поста"""
        return self.views.count()

    class Meta:
        ordering = ['-created']  # Сортировка постов от новых к старым


# Модель комментариев к постам
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)  # Пост, к которому относится комментарий
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Автор комментария
    content = models.TextField(verbose_name='Комментарий')  # Содержание комментария
    created = models.DateTimeField(auto_now_add=True)  # Дата создания комментария
    available = models.BooleanField(default=True, verbose_name='Активный/Неактивный')  # Доступность комментария

    class Meta:
        ordering = ['-created']  # Сортировка комментариев от новых к старым

    def __str__(self):
        return self.author.username + ' | ' + self.post.title  # Возвращает строку вида "Автор | Заголовок поста"
