from django.urls import path
from .views import SiteLoginView, register_view
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('login/', SiteLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
]
