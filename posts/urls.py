from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostList, name='posts'),
    path('create/', views.PostCreateView.as_view(), name='postCreate'),
    path('update/<slug:slug>/', views.PostUpdateView.as_view(), name='postUpdate'),
    path('delete/<int:pk>/', views.PostDeleteView.as_view(), name='postDelete'),

    # Категории и теги
    path('categories/<slug:category_slug>/', views.PostList, name='posts_by_category'),
    path('tags/<slug:tag_slug>/', views.PostList, name='posts_by_tag'),

    # Детальный просмотр поста (исправлен путь, убрано `post/post/`)
    path('post/<slug:post_category_slug>/<int:pk>/<slug:slug>/', views.PostDetailView.as_view(), name='postDetail'),

    path('search/', views.search, name='search'),
    path('comment/<int:pk>/', views.CommentView.as_view(), name='addComment'),
]
