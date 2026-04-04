"""Административная панель для приложения меню"""
from django.contrib import admin
from .models import Category, MenuItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order']


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'order']
    list_filter = ['category', 'is_available']
    list_editable = ['price', 'is_available', 'order']
    search_fields = ['name', 'description']
