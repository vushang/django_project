from django.contrib import messages  # Модуль для работы с уведомлениями
from django.contrib.auth import authenticate, login, logout  # Функции для аутентификации и выхода
from django.contrib.auth.forms import PasswordChangeForm  # Форма смены пароля
from django.contrib.auth.mixins import LoginRequiredMixin  # Миксин для ограничения доступа авторизованным пользователям
from django.contrib.auth.models import User  # Модель пользователя Django
from django.contrib.auth.views import PasswordChangeView  # Класс для смены пароля
from django.db.models import Count  # Функция для подсчета количества объектов в запросе
from django.http import HttpResponseRedirect  # Класс для редиректа
from django.shortcuts import render, redirect, get_object_or_404  # Функции рендеринга и получения объекта
from django.urls import reverse_lazy  # Функция для получения ленивого URL
from django.views.generic import TemplateView  # Базовый шаблонный класс представления
from django.views.generic.detail import DetailView  # Класс представления для детального просмотра
from django.views.generic.list import ListView, MultipleObjectMixin  # Классы представлений списка и поддержки нескольких объектов

from posts.models import Post, Category, Tag  # Импорт моделей постов, категорий и тегов
from .forms import UserDetailForm, UserForm  # Импорт пользовательских форм


# Представление для отображения профиля пользователя
class ProfileDetailView(LoginRequiredMixin, MultipleObjectMixin, DetailView):
    model = User
    template_name = 'profile.html'
    paginate_by = 8  # Количество объектов на странице

    def get_object(self):
        """Возвращает текущего авторизованного пользователя"""
        request_user = get_object_or_404(User, username=self.request.user.username)
        return request_user

    def get_context_data(self, **kwargs):
        """Добавляет в контекст список постов пользователя, категории, теги и популярные посты"""
        object_list = Post.objects.filter(available=True, author=self.request.user)
        context = super(ProfileDetailView, self).get_context_data(object_list=object_list, **kwargs)
        context['popularposts'] = Post.objects.filter(available=True).annotate(viewyek=Count('views')).order_by('-viewyek')[:3]
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context


# Представление для смены пароля пользователя
class PasswordsChangeView(PasswordChangeView):
    template_name = 'change-password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('user:viewProfile')

    def form_valid(self, form):
        """Добавляет сообщение об успешной смене пароля"""
        messages.success(self.request, "Your password has been changed successfully.")
        return super(PasswordsChangeView, self).form_valid(form)


# Представление для обновления профиля пользователя
class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    profile_form = UserDetailForm
    template_name = 'profile_update.html'

    def post(self, request):
        """Обрабатывает отправленную форму и обновляет данные профиля"""
        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = UserDetailForm(post_data, file_data, instance=request.user.userdetail)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return HttpResponseRedirect(reverse_lazy('user:updateProfile'))

        context = self.get_context_data(user_form=user_form, profile_form=profile_form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        """Обрабатывает GET-запрос аналогично POST-запросу"""
        return self.post(request)


# Представление для регистрации нового пользователя
def registerView(request):
    if request.method == 'POST':
        # Получаем данные из формы регистрации
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST['repassword']

        # Проверяем совпадение паролей
        if password == repassword:
            # Проверяем, занят ли уже логин или email
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                messages.warning(request, 'Username or email is already taken.')
                return redirect('user:register')
            else:
                # Создаем нового пользователя
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Registration created! You can login to your account.')
                return redirect('user:login')
        else:
            messages.warning(request, 'Passwords do not match.')
            return redirect('user:register')
    else:
        return render(request, 'register.html')


# Представление для входа в систему
def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)  # Проверяем учетные данные
        if user is not None:
            login(request, user)  # Выполняем вход
            messages.success(request, 'Login successful! Welcome, ' + username)
            return redirect('pages:index')
        else:
            messages.error(request, 'Check your information and try again!')
            return redirect('user:login')
    else:
        return render(request, 'login.html')


# Представление для выхода из системы
def logoutView(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('user:login')


# Представление для отображения списка авторов с их количеством постов
class AuthorIndexView(ListView):
    paginate_by = 8  # Количество объектов на странице
    model = User
    context_object_name = 'author_list'
    template_name = 'authors.html'
    post = Post.objects.filter(available=True).count()
    queryset = User.objects.annotate(total_posts=Count('post')).filter(total_posts__gt='0').order_by('-total_posts')  # Отображаются только авторы с постами

    def get_context_data(self, **kwargs):
        """Добавляет в контекст популярные посты, категории и теги"""
        context = super().get_context_data(**kwargs)
        context['popularposts'] = Post.objects.filter(available=True).annotate(viewyek=Count('views')).order_by('-viewyek')[:3]
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context


# Представление для отображения детальной информации об авторе
class AuthorDetailView(DetailView, MultipleObjectMixin):
    model = User
    template_name = 'author_detail.html'
    context_object_name = 'author'
    paginate_by = 8  # Количество объектов на странице

    def get_context_data(self, **kwargs):
        """Добавляет в контекст список постов автора, категории, теги и популярные посты"""
        object_list = Post.objects.filter(available=True, author=self.get_object())
        context = super(AuthorDetailView, self).get_context_data(object_list=object_list, **kwargs)
        context['popularposts'] = Post.objects.filter(available=True).annotate(viewyek=Count('views')).order_by('-viewyek')[:3]
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context
