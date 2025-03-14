# Generated by Django 3.1.7 on 2025-03-02 10:15

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название категории')),
                ('slug', models.SlugField(help_text='Рекомендуется не изменять это вручную.', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='HitCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название тега')),
                ('slug', models.SlugField(help_text='Рекомендуется не изменять это вручную.', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=75, verbose_name='Заголовок')),
                ('slug', models.SlugField(help_text='Рекомендуется не изменять это вручную.', unique=True)),
                ('image', models.ImageField(upload_to='posts/%Y/%m/%d/', verbose_name='Изображение')),
                ('content', ckeditor.fields.RichTextField(verbose_name='Контент')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('available', models.BooleanField(default=True, verbose_name='Активный/Неактивный')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.category')),
                ('tags', models.ManyToManyField(blank=True, to='posts.Tag', verbose_name='Теги')),
                ('views', models.ManyToManyField(blank=True, related_name='post_views', to='posts.HitCount')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Комментарий')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('available', models.BooleanField(default=True, verbose_name='Активный/Неактивный')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.post')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
