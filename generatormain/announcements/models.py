from django.db import models
from django.contrib.auth.models import User


class Announcement(models.Model):
    TYPE_NEWS = 'news'
    TYPE_ANNOUNCEMENT = 'announcement'
    TYPE_CHOICES = [
        (TYPE_NEWS, 'Новина'),
        (TYPE_ANNOUNCEMENT, 'Оголошення'),
    ]

    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='announcements', verbose_name='Автор'
    )
    announcement_type = models.CharField(
        max_length=20, choices=TYPE_CHOICES,
        default=TYPE_ANNOUNCEMENT, verbose_name='Тип'
    )
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Зміст')
    image = models.ImageField(
        upload_to='announcements/', blank=True, null=True, verbose_name='Зображення'
    )
    is_published = models.BooleanField(default=True, verbose_name='Опубліковано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')

    class Meta:
        verbose_name = 'Оголошення'
        verbose_name_plural = 'Оголошення'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
