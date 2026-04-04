"""URL-маршруты бронирований"""
from django.urls import path
from .views import ContactView

app_name = 'orders'

urlpatterns = [
    path('contacts/', ContactView.as_view(), name='contacts'),
]
