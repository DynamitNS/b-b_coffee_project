"""Модели для бронирования столиков"""
from django.db import models


class Reservation(models.Model):
    """Заявка на бронирование столика"""
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('confirmed', 'Подтверждена'),
        ('cancelled', 'Отменена'),
    ]

    name = models.CharField('Имя', max_length=200)
    email = models.EmailField('Email')
    message = models.TextField('Сообщение', blank=True)
    status = models.CharField(
        'Статус', max_length=20,
        choices=STATUS_CHOICES, default='new'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.email} ({self.get_status_display()})'
