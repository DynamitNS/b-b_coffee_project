"""Модели для приложения меню"""
from django.db import models


class Category(models.Model):
    """Категория позиций меню (Кофе, Десерты и т.д.)"""
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('URL-имя', unique=True)
    order = models.PositiveIntegerField('Порядок отображения', default=0)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """Позиция в меню кофейни"""
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        verbose_name='Категория', related_name='items'
    )
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2)
    image = models.ImageField('Фото', upload_to='menu_items/', blank=True, null=True)
    is_available = models.BooleanField('Доступно', default=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Позиция меню'
        verbose_name_plural = 'Позиции меню'
        ordering = ['category__order', 'order', 'name']

    def __str__(self):
        return f'{self.name} — {self.price} ₽'
