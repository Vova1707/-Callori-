from django.db import models
from django.contrib.auth.models import AbstractUser
from .utilities import get_timestamp_path

class User(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name="Вы прошли активацию?")
    send_message = models.BooleanField(default=True, verbose_name="Присылать вам оповещения о комментариях?")

    def delete(self, *args, **kwargs):
        for bb in self.posted_set.all():
            bb.delete()
        super().delete(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass


class Posted(models.Model):
    title = models.CharField(max_length=40, verbose_name='Название поста')
    content = models.TextField(verbose_name='Описание')
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Изображение')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор объявления')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Выводить в списке?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
            super().delete(*args, **kwargs)
    class Meta:
        verbose_name_plural = 'Пост'
        verbose_name = 'Посты'
        ordering = ['-created_at']


class AdditionalImage(models.Model):
    bb = models.ForeignKey(Posted, on_delete=models.CASCADE, verbose_name='Пост')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Изображение')
    class Meta:
        verbose_name_plural = 'Дополнительные иллюстрации'
        verbose_name = 'Дополнительная иллюстрация'