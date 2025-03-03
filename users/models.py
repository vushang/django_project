from django.contrib.auth.models import User  
from django.db import models  
from django.db.models.signals import post_save  
from django.dispatch import receiver  


# Определяем модель UserDetail, которая хранит дополнительную информацию о пользователе.
class UserDetail(models.Model):
    # Связь "один к одному" с моделью User. 
    # Если пользователь удаляется, удаляется и связанный объект UserDetail.
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    
    # Дополнительные поля для пользователя: заголовок и описание.
    title = models.CharField(blank=True, null=True, max_length=50, verbose_name="Заголовок")
    description = models.CharField(blank=True, null=True, max_length=250, verbose_name="Описание")
    
    # Поле для загрузки изображения пользователя, сохраняемого в папке "users/"
    # Если изображение не указано, используется значение по умолчанию "def_user.png".
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to="users/",
        default="def_user.png",
        verbose_name="Изображение"
    )

    # Сигнал для автоматического создания объекта UserDetail при создании нового пользователя.
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        """
        Функция-обработчик сигнала post_save.
        Вызывается каждый раз, когда создаётся новый пользователь (User).
        Если пользователь новый (created=True), создаём для него объект UserDetail.
        """
        if created:
            UserDetail.objects.create(user=instance)

    # Сигнал для автоматического сохранения профиля пользователя при обновлении User.
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        """
        Функция-обработчик сигнала post_save.
        Вызывается после сохранения объекта User.
        Обновляет связанный объект UserDetail.
        """
        instance.userdetail.save()


    def __str__(self):
        return self.user.username
