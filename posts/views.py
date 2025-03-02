from django.contrib import messages  # Импортируем модуль сообщений Django
from django.contrib.auth.decorators import login_required  # Декоратор для проверки авторизации пользователя
from django.contrib.auth.mixins import LoginRequiredMixin  # Миксин для классов представлений, требующих авторизации
from django.core.paginator import Paginator  # Класс для разбивки списка объектов на страницы
from django.db.models import Count, Q  # Импорт агрегатных функций для работы с базой данных
from django.http import Http404  # Исключение для обработки отсутствующих страниц
from django.shortcuts import get_object_or_404, render  # Функции для рендеринга страниц и получения объектов
from django.template.defaultfilters import slugify  # Фильтр для создания slug (ЧПУ)
from django.urls import reverse, reverse_lazy  # Функции для генерации URL-адресов
from django.utils.decorators import method_decorator  # Импорт декоратора для использования в классах
from django.views.generic.detail import DetailView  # Детальное представление объекта
from django.views.generic.edit import CreateView, UpdateView, DeleteView  # Классы для CRUD-операций

from .models import Post, Category, Tag, HitCount, Comment  # Импортируем модели


class CommentView(LoginRequiredMixin, CreateView):
    """
    Представление для создания комментария.
    Требует авторизации.
    """
    template_name = 'comment_create.html'
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        """Добавляет автора комментария и привязывает его к посту"""
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']
        messages.success(self.request, 'Комментарий успешно добавлен.')
        return super().form_valid(form)

    def get_success_url(self):
        """После успешного создания перенаправляет на страницу поста"""
        return reverse('posts:postDetail', args=(self.object.post.category.slug, self.object.post.pk, self.object.post.slug))


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания поста.
    Требует авторизации.
    """
    template_name = 'post_create.html'
    model = Post
    fields = ['category', 'tags', 'title', 'image', 'content']

    def form_valid(self, form):
        """Создаёт slug и сохраняет пост"""
        post = form.save(commit=False)
        post.author = self.request.user
        post.slug = slugify(post.title) or f'post-{post.pk}'

        counter = 1
        temp_slug = post.slug
        while Post.objects.filter(slug=post.slug).exists():
            post.slug = f'{temp_slug}-{counter}'
            counter += 1

        post.save()
        messages.success(self.request, 'Ваш пост успешно создан.')
        return super().form_valid(form)

    def get_success_url(self):
        """После создания перенаправляет на детальную страницу поста"""
        return reverse('posts:postDetail', args=(self.object.category.slug, self.object.pk, self.object.slug))


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для обновления поста.
    Требует авторизации и проверки, что пользователь является автором поста.
    """
    model = Post
    template_name = 'post_update.html'
    template_name_suffix = '_update_form'
    fields = ['category', 'tags', 'title', 'image', 'content']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """Проверяет, что текущий пользователь является автором поста"""
        post = self.get_object()
        if post.author != self.request.user:
            raise Http404("Вы не можете редактировать этот пост")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Обновляет slug, если он отсутствует"""
        post = form.save(commit=False)
        if not post.slug:
            post.slug = slugify(post.title)

        counter = 1
        temp_slug = post.slug
        while Post.objects.filter(slug=post.slug).exclude(id=post.id).exists():
            post.slug = f'{temp_slug}-{counter}'
            counter += 1

        post.save()
        messages.success(self.request, 'Ваш пост успешно обновлен.')
        return super().form_valid(form)

    def get_success_url(self):
        """После обновления перенаправляет на детальную страницу поста"""
        return reverse('posts:postDetail', args=(self.object.category.slug, self.object.pk, self.object.slug))


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления поста.
    Требует авторизации и проверки, что пользователь является автором поста.
    """
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('user:viewProfile')

    def get_object(self, queryset=None):
        """Проверяет, что текущий пользователь является автором поста"""
        post = super().get_object()
        if post.author != self.request.user:
            raise Http404("Вы не можете удалить этот пост")
        return post

    def delete(self, request, *args, **kwargs):
        """Добавляет сообщение об успешном удалении поста"""
        messages.success(self.request, 'Пост успешно удален.')
        return super().delete(request, *args, **kwargs)


def PostList(request, category_slug=None, tag_slug=None):
    """
    Представление для вывода списка постов.
    Может фильтровать по категории или тегу.
    """
    category_page = None
    tag_page = None
    categories = Category.objects.all()
    tags = Tag.objects.all()
    popularposts = Post.objects.filter(available=True).annotate(viewyek=Count('views')).order_by('-viewyek')[:3]
    context = {}

    if category_slug:
        category_page = get_object_or_404(Category, slug=category_slug)
        posts = Post.objects.filter(available=True, category=category_page).order_by('-created')
        context['title'] = 'Посты по категории'
    elif tag_slug:
        tag_page = get_object_or_404(Tag, slug=tag_slug)
        posts = Post.objects.filter(available=True, tags=tag_page).order_by('-created')
        context['title'] = 'Посты по тегу'
    else:
        posts = Post.objects.filter(available=True).order_by('-created')
        context['title'] = 'Все посты'

    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    post_list = paginator.get_page(page_number)

    context.update({
        'post_list': post_list,
        'popularposts': popularposts,
        'categories': categories,
        'tags': tags,
    })
    return render(request, 'posts.html', context)


def get_client_ip(request):
    """
    Функция для получения IP-адреса клиента.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class PostDetailView(DetailView):
    """
    Представление для детального просмотра поста.
    """
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        """Добавляет в контекст популярные, похожие посты, категории, теги и комментарии"""
        context = super().get_context_data(**kwargs)
        context['popularposts'] = Post.objects.filter(available=True).annotate(viewyek=Count('views')).order_by('-viewyek')[:3]
        context['relatedposts'] = Post.objects.filter(available=True, category=self.object.category).annotate(viewyek=Count('views')).order_by('-viewyek')[:3]
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        context['comments'] = Comment.objects.filter(available=True, post=self.object).order_by('-created')[:10]
        return context

    def get(self, request, *args, **kwargs):
            """Добавляет просмотр поста и увеличивает количество просмотров при каждом заходе"""
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)

            ip = get_client_ip(self.request)

            # Создаём новый объект HitCount для каждого запроса
            hit = HitCount.objects.create(ip=ip)
            self.object.views.add(hit)  # Добавляем его в список просмотров поста

            return self.render_to_response(context)

def search(request):
    """
    Функция поиска постов по заголовку или содержимому.
    """
    query = request.GET.get('query', '').strip()
    posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    categories = Category.objects.all()
    tags = Tag.objects.all()

    context = {
        'post_list': posts,
        'categories': categories,
        'tags': tags,
        'title': 'Результаты поиска'
    }
    return render(request, 'posts.html', context)
