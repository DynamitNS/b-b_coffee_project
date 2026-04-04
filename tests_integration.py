"""
Интеграционные тесты проекта bb_coffee (ПР №13 — Интеграционное тестирование)

Проверяют взаимодействие между приложениями, сквозные пользовательские сценарии
и корректность работы всей системы в целом.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal
from menu.models import Category, MenuItem
from orders.models import Reservation


User = get_user_model()


# ─────────────────────────────────────────────
# ИНТЕГРАЦИЯ: НАВИГАЦИЯ МЕЖДУ СТРАНИЦАМИ
# ─────────────────────────────────────────────

class NavigationIntegrationTest(TestCase):
    """Сквозная навигация по сайту"""

    def setUp(self):
        self.client = Client()

    def test_all_pages_return_200(self):
        """Все три основные страницы доступны"""
        urls = [
            reverse('pages:index'),
            reverse('menu:menu'),
            reverse('orders:contacts'),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f'Страница {url} недоступна')

    def test_menu_link_in_index(self):
        """Главная содержит ссылку на меню"""
        response = self.client.get(reverse('pages:index'))
        self.assertContains(response, reverse('menu:menu'))

    def test_contacts_link_in_index(self):
        """Главная содержит ссылку на контакты"""
        response = self.client.get(reverse('pages:index'))
        self.assertContains(response, reverse('orders:contacts'))

    def test_footer_present_on_all_pages(self):
        """Подвал присутствует на всех страницах"""
        urls = [reverse('pages:index'), reverse('menu:menu'), reverse('orders:contacts')]
        for url in urls:
            response = self.client.get(url)
            self.assertContains(response, 'site-footer', msg_prefix=f'Нет подвала на {url}')


# ─────────────────────────────────────────────
# ИНТЕГРАЦИЯ: МЕНЮ — БД — ШАБЛОН
# ─────────────────────────────────────────────

class MenuIntegrationTest(TestCase):
    """Интеграция: меню отображается из БД"""

    def setUp(self):
        self.client = Client()
        self.cat_coffee = Category.objects.create(name='Кофе', slug='coffee', order=1)
        self.cat_food = Category.objects.create(name='Десерты', slug='desserts', order=2)

        MenuItem.objects.create(
            category=self.cat_coffee, name='Эспрессо',
            price=Decimal('190.00'), is_available=True,
            description='Классика бариста'
        )
        MenuItem.objects.create(
            category=self.cat_coffee, name='Латте',
            price=Decimal('280.00'), is_available=True,
        )
        MenuItem.objects.create(
            category=self.cat_food, name='Тирамису',
            price=Decimal('380.00'), is_available=True,
            description='Итальянский десерт'
        )
        # Недоступная позиция — не должна отображаться
        MenuItem.objects.create(
            category=self.cat_coffee, name='Секретный напиток',
            price=Decimal('999.00'), is_available=False
        )

    def test_categories_appear_on_menu_page(self):
        """Категории из БД отображаются на странице"""
        response = self.client.get(reverse('menu:menu'))
        self.assertContains(response, 'Кофе')
        self.assertContains(response, 'Десерты')

    def test_items_appear_on_menu_page(self):
        """Все доступные позиции отображаются"""
        response = self.client.get(reverse('menu:menu'))
        self.assertContains(response, 'Эспрессо')
        self.assertContains(response, 'Латте')
        self.assertContains(response, 'Тирамису')

    def test_unavailable_item_hidden(self):
        """Недоступная позиция не отображается"""
        response = self.client.get(reverse('menu:menu'))
        self.assertNotContains(response, 'Секретный напиток')

    def test_descriptions_displayed(self):
        """Описания отображаются на странице"""
        response = self.client.get(reverse('menu:menu'))
        self.assertContains(response, 'Классика бариста')
        self.assertContains(response, 'Итальянский десерт')

    def test_prices_displayed(self):
        """Цены отображаются на странице"""
        response = self.client.get(reverse('menu:menu'))
        self.assertContains(response, '190')
        self.assertContains(response, '380')

    def test_empty_menu_no_crash(self):
        """Пустое меню не вызывает ошибку"""
        MenuItem.objects.all().delete()
        Category.objects.all().delete()
        response = self.client.get(reverse('menu:menu'))
        self.assertEqual(response.status_code, 200)


# ─────────────────────────────────────────────
# ИНТЕГРАЦИЯ: ФОРМА → БД → РЕДИРЕКТ
# ─────────────────────────────────────────────

class ReservationFlowTest(TestCase):
    """Интеграция: полный цикл бронирования"""

    def setUp(self):
        self.client = Client()
        self.url = reverse('orders:contacts')

    def test_full_reservation_flow(self):
        """Сквозной сценарий: заполнение формы → сохранение → редирект → подтверждение"""
        # 1. Открываем страницу
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

        # 2. Отправляем форму
        data = {
            'name': 'Мария Петрова',
            'email': 'maria@example.com',
            'message': 'Хочу забронировать столик на день рождения'
        }
        response = self.client.post(self.url, data)

        # 3. Проверяем редирект
        self.assertEqual(response.status_code, 302)
        self.assertIn('ok=1', response['Location'])

        # 4. Запись в БД
        reservation = Reservation.objects.get(email='maria@example.com')
        self.assertEqual(reservation.name, 'Мария Петрова')
        self.assertEqual(reservation.status, 'new')

        # 5. Страница подтверждения показывает success-баннер
        response = self.client.get(response['Location'])
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['success'])
        self.assertContains(response, 'Заявка принята')

    def test_multiple_reservations_saved_independently(self):
        """Несколько бронирований сохраняются независимо"""
        for i in range(3):
            self.client.post(self.url, {
                'name': f'Гость {i}',
                'email': f'guest{i}@test.ru',
                'message': 'Тест'
            })
        self.assertEqual(Reservation.objects.count(), 3)

    def test_reservation_with_empty_message(self):
        """Бронирование без сообщения сохраняется"""
        self.client.post(self.url, {
            'name': 'Без сообщения',
            'email': 'nomsg@test.ru',
            'message': ''
        })
        self.assertTrue(Reservation.objects.filter(email='nomsg@test.ru').exists())


# ─────────────────────────────────────────────
# ИНТЕГРАЦИЯ: АДМИНИСТРАТИВНАЯ ПАНЕЛЬ
# ─────────────────────────────────────────────

class AdminIntegrationTest(TestCase):
    """Интеграция: административная панель"""

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            'Admin', 'admin@test.ru', 'admin123'
        )
        self.category = Category.objects.create(name='Кофе', slug='coffee', order=1)

    def test_admin_login(self):
        """Суперпользователь входит в админ-панель"""
        self.client.login(username='Admin', password='admin123')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

    def test_admin_can_see_menu_items(self):
        """Администратор видит позиции меню"""
        MenuItem.objects.create(
            category=self.category, name='Капучино',
            price=Decimal('270.00')
        )
        self.client.login(username='Admin', password='admin123')
        response = self.client.get('/admin/menu/menuitem/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Капучино')

    def test_admin_can_see_reservations(self):
        """Администратор видит бронирования"""
        Reservation.objects.create(name='Тест', email='t@t.ru')
        self.client.login(username='Admin', password='admin123')
        response = self.client.get('/admin/orders/reservation/')
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_admin_redirects(self):
        """Неавторизованный пользователь перенаправляется"""
        response = self.client.get('/admin/')
        self.assertIn(response.status_code, [301, 302])


# ─────────────────────────────────────────────
# ИНТЕГРАЦИЯ: БЕЗОПАСНОСТЬ (ПР №14, №15, №17)
# ─────────────────────────────────────────────

class SecurityTest(TestCase):
    """Тесты безопасности (ПР №14 Анализ рисков, ПР №15 Безопасность backend)"""

    def setUp(self):
        self.client = Client()

    def test_csrf_protection_on_form(self):
        """CSRF-защита активна на форме бронирования"""
        # Запрос без CSRF-токена (enforce_csrf_checks=True)
        client_no_csrf = Client(enforce_csrf_checks=True)
        response = client_no_csrf.post(reverse('orders:contacts'), {
            'name': 'Хакер', 'email': 'h@h.ru', 'message': ''
        })
        self.assertEqual(response.status_code, 403)

    def test_admin_not_accessible_without_login(self):
        """Админ-панель недоступна без авторизации"""
        response = self.client.get('/admin/menu/menuitem/')
        self.assertIn(response.status_code, [301, 302])

    def test_xss_in_reservation_name(self):
        """XSS-инъекция в имени не выполняется"""
        self.client.post(reverse('orders:contacts'), {
            'name': '<script>alert(1)</script>',
            'email': 'xss@test.ru',
            'message': ''
        })
        r = Reservation.objects.get(email='xss@test.ru')
        # Данные сохраняются как есть — экранирование на уровне шаблона
        response = self.client.get(reverse('orders:contacts') + '?ok=1')
        self.assertNotContains(response, '<script>alert(1)</script>')
