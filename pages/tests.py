"""
Модульные тесты приложения pages (ПР №12 — Модульное тестирование)
"""
from django.test import TestCase, Client
from django.urls import reverse


class IndexViewTest(TestCase):
    """Тесты главной страницы"""

    def setUp(self):
        self.client = Client()

    def test_index_returns_200(self):
        """Главная страница доступна"""
        response = self.client.get(reverse('pages:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_uses_correct_template(self):
        """Используется корректный шаблон"""
        response = self.client.get(reverse('pages:index'))
        self.assertTemplateUsed(response, 'pages/index.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_index_contains_brand_name(self):
        """Главная содержит название бренда"""
        response = self.client.get(reverse('pages:index'))
        self.assertContains(response, 'B&amp;B COFFEE')

    def test_index_contains_hero_text(self):
        """Главная содержит текст hero-блока"""
        response = self.client.get(reverse('pages:index'))
        self.assertContains(response, 'возвращаются')

    def test_nav_links_present(self):
        """Навигационные ссылки присутствуют"""
        response = self.client.get(reverse('pages:index'))
        self.assertContains(response, '/menu/')
        self.assertContains(response, '/orders/contacts/')
