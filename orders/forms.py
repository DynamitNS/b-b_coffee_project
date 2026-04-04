"""Форма бронирования столика"""
from django import forms
from .models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя', 'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ваш Email', 'class': 'form-input'}),
            'message': forms.Textarea(attrs={'placeholder': 'Ваш запрос', 'class': 'form-textarea', 'rows': 4}),
        }
        labels = {
            'name': '',
            'email': '',
            'message': '',
        }
