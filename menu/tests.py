"""
Модульные тесты приложения menu (ПР №12 — Модульное тестирование)
Покрывают: модели Category и MenuItem, вьюхи, URL-маршруты
"""
from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from .models import Category, MenuItem


# ─────────────────────────────────────────────
# МОДУЛЬНЫЕ ТЕСТЫ МОДЕЛЕЙ
# ─────────────────────────────────────────────

class CategoryModelTest(TestCase):
    """Тесты модели Category"""

    def setUp(self):
        self.category = Category.objects.create(
            name='Кофе', slug='coffee', order=1
        )

    def test_str_representation(self):
        """__str__ возвращает название категории"""
        self.assertEqual(str(self.category), 'Кофе')

    def test_category_fields(self):
        """Поля категории сохраняются корректно"""
        self.assertEqual(self.category.slug, 'coffee')
        self.assertEqual(self.category.order, 1)

    def test_category_ordering(self):
        """Категории сортируются по полю order"""
        Category.objects.create(name='Десерты', slug='desserts', order=2)
        cats = list(Category.objects.values_list('name', flat=True))
        self.assertEqual(cats[0], 'Кофе')
        self.assertEqual(cats[1], 'Десерты')

    def test_slug_unique(self):
        """Slug уникален"""
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Category.objects.create(name='Кофе2', slug='coffee', order=99)


class MenuItemModelTest(TestCase):
    """Тесты модели MenuItem"""

    def setUp(self):
        self.category = Category.objects.create(
            name='Кофе', slug='coffee', order=1
        )
        self.item = MenuItem.objects.create(
            category=self.category,
            name='Эспрессо',
            description='Концентрированный напиток',
            price=Decimal('190.00'),
            is_available=True,
            order=0
        )

    def test_str_representation(self):
        """__str__ содержит название и цену"""
        self.assertIn('Эспрессо', str(self.item))
        self.assertIn('190', str(self.item))

    def test_default_is_available(self):
        """По умолчанию позиция доступна"""
        item = MenuItem.objects.create(
            category=self.category,
            name='Латте',
            price=Decimal('280.00')
        )
        self.assertTrue(item.is_available)

    def test_item_belongs_to_category(self):
        """Позиция принадлежит категории"""
        self.assertEqual(self.item.category, self.category)

    def test_price_decimal(self):
        """Цена хранится как Decimal"""
        self.assertEqual(self.item.price, Decimal('190.00'))

    def test_item_without_description(self):
        """Позиция может быть без описания"""
        item = MenuItem.objects.create(
            category=self.category,
            name='Капучино',
            price=Decimal('270.00'),
            description=''
        )
        self.assertEqual(item.description, '')

    def test_unavailable_item(self):
        """Недоступные позиции фильтруются"""
        self.item.is_available = False
        self.item.save()
        available = MenuItem.objects.filter(is_available=True)
        self.assertNotIn(self.item, available)


# ─────────────────────────────────────────────
# МОДУЛЬНЫЕ ТЕСТЫ ВЬЮХ (UNIT)
# ─────────────────────────────────────────────

class MenuViewTest(TestCase):
    """Тесты вьюхи страницы меню"""

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name='Кофе', slug='coffee', order=1
        )
        MenuItem.objects.create(
            category=self.category, name='Эспрессо',
            price=Decimal('190.00'), is_available=True
        )
        MenuItem.objects.create(
            category=self.category, name='Скрытый',
            price=Decimal('100.00'), is_available=False
        )

    def test_menu_page_status_200(self):
        """Страница меню возвращает 200"""
        response = self.client.get(reverse('menu:menu'))
        self.assertEqual(response.status_code, 200)

    def test_menu_uses_correct_template(self):
        """Используется шаблон menu/menu.html"""
        response = self.client.get(reverse('menu:menu'))
        self.assertTemplateUsed(response, 'menu/menu.html')

    def test_menu_context_has_categories(self):
        """Контекст содержит categories"""
        response = self.client.get(reverse('menu:menu'))
        self.assertIn('categories', response.context)

    def test_menu_shows_available_items_only(self):
        """На странице только доступные позиции"""
        response = self.client.get(reverse('menu:menu'))
        self.assertContains(response, 'Эспрессо')
        self.assertNotContains(response, 'Скрытый')

    def test_menu_shows_price(self):
        """Цена отображается на странице"""
        response = self.client.get(reverse('menu:menu'))
        self.assertContains(response, '190')

    def test_menu_search_by_query(self):
        """Поиск по названию фильтрует результаты"""
        response = self.client.get(reverse('menu:menu'), {'q': 'Эспрессо'})
        self.assertContains(response, 'Эспрессо')
        self.assertNotContains(response, 'Скрытый')

    def test_menu_filter_by_category(self):
        """Фильтр по категории показывает только выбранную категорию"""
        response = self.client.get(reverse('menu:menu'), {'category': 'coffee'})
        self.assertContains(response, 'Эспрессо')
        self.assertNotContains(response, 'Скрытый')
