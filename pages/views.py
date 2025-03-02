import random  # Импортируем модуль для работы со случайными числами
import re  # Импортируем модуль для работы с регулярными выражениями

from django.contrib import messages  # Модуль для работы с уведомлениями пользователю
from django.db.models import Count  # Функция для подсчёта количества объектов
from django.shortcuts import render  # Функция рендеринга HTML-шаблонов
from django.views.generic.list import ListView  # Класс для создания представления списка объектов
from django.core.mail import EmailMessage  # Класс для отправки email-сообщений
from django.conf import settings  # Импорт настроек Django

from posts.models import Post, Category, Tag  # Импортируем модели


class LatestPostListView(ListView):
    """
    Представление для отображения последних постов на главной странице.
    """
    model = Post
    template_name = 'index.html'
    context_object_name = 'latestposts'
    queryset = Post.objects.filter(available=True).order_by('-created')[:6]  # Получаем последние 6 постов

    def get_context_data(self, **kwargs):
        """Добавляет в контекст популярные, случайные посты, категории и теги."""
        context = super().get_context_data(**kwargs)

        # Получаем общее количество постов
        post_count = Post.objects.filter(available=True).count()

        # Выбираем 3 случайных поста, если их достаточно
        if post_count >= 3:
            items = list(Post.objects.filter(available=True))
            random_items = random.sample(items, 3)
            context['randomposts'] = random_items
        else:
            context['randomposts'] = Post.objects.filter(available=True)

        # Популярные посты (на основе количества просмотров)
        context['popularposts'] = Post.objects.filter(available=True).annotate(viewyek=Count('views')).order_by('-viewyek')[:3]

        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context


class AboutView(ListView):
    """
    Представление для страницы "О нас".
    """
    model = Post
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        """Добавляет в контекст популярные посты, категории и теги."""
        context = super().get_context_data(**kwargs)

        # Популярные посты (на основе количества просмотров)
        context['popularposts'] = Post.objects.filter(available=True).annotate(viewyek=Count('views')).order_by('-viewyek')[:3]

        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context


def is_valid_email(email):
    """
    Функция валидации email с помощью регулярного выражения.
    """
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email)


def ContactView(request):
    """
    Представление для страницы обратной связи (контактов).
    """
    categories = Category.objects.all()
    tags = Tag.objects.all()
    popularposts = Post.objects.filter(available=True).annotate(viewyek=Count('views')).order_by('-viewyek')[:3]

    context = {
        'popularposts': popularposts,
        'categories': categories,
        'tags': tags,
    }

    if request.method == 'POST':
        # Получаем данные из формы и убираем пробелы по краям
        subject = request.POST.get('subject', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        # Проверяем, что все поля заполнены
        if not subject or not email or not message:
            messages.error(request, 'Все поля должны быть заполнены!')
            return render(request, 'contact.html', context)

        # Проверяем корректность email
        if not is_valid_email(email):
            messages.error(request, 'Введите корректный email!')
            return render(request, 'contact.html', context)

        recipient_email = email  # Кому отправлять письмо

        try:
            # Отправляем email
            email_message = EmailMessage(
                subject=subject,
                body=f"Email: {email}\n\nMessage:\n{message}",
                from_email=settings.EMAIL_HOST_USER,
                to=[recipient_email]
            )
            email_message.send(fail_silently=False)
            messages.success(request, 'Ваше сообщение успешно отправлено!')
        except Exception as e:
            messages.error(request, f'Ошибка отправки email: {e}')

    return render(request, 'contact.html', context)
