"""Вьюхи для основных страниц сайта"""
from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Главная страница"""
    template_name = 'pages/index.html'
