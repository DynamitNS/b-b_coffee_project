"""Административная панель для бронирований"""
from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'status', 'created_at']
    list_filter = ['status']
    list_editable = ['status']
    readonly_fields = ['created_at']
