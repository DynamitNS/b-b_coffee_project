"""
Модульные тесты приложения orders (ПР №12 — Модульное тестирование)
Покрывают: модель Reservation, форму ReservationForm, вьюху ContactView
"""
from django.test import TestCase, Client
from django.urls import reverse
from .models import Reservation
from .forms import ReservationForm


# ─────────────────────────────────────────────
# МОДУЛЬНЫЕ ТЕСТЫ МОДЕЛИ
# ─────────────────────────────────────────────

class ReservationModelTest(TestCase):
    """Тесты модели Reservation"""

    def setUp(self):
        self.reservation = Reservation.objects.create(
            name='Иван Иванов',
            email='ivan@test.ru',
            message='Хочу забронировать столик на 2 человека'
        )

    def test_str_representation(self):
        """__str__ содержит имя и email"""
        s = str(self.reservation)
        self.assertIn('Иван Иванов', s)
        self.assertIn('ivan@test.ru', s)

    def test_default_status_is_new(self):
        """Статус по умолчанию — 'new'"""
        self.assertEqual(self.reservation.status, 'new')

    def test_created_at_set_automatically(self):
        """Дата создания проставляется автоматически"""
        self.assertIsNotNone(self.reservation.created_at)

    def test_status_choices(self):
        """Все допустимые статусы принимаются"""
        for status_code, _ in Reservation.STATUS_CHOICES:
            self.reservation.status = status_code
            self.reservation.save()
            self.assertEqual(
                Reservation.objects.get(pk=self.reservation.pk).status,
                status_code
            )

    def test_message_optional(self):
        """Сообщение не обязательно"""
        r = Reservation.objects.create(name='Петр', email='p@test.ru')
        self.assertEqual(r.message, '')


# ─────────────────────────────────────────────
# МОДУЛЬНЫЕ ТЕСТЫ ФОРМЫ
# ─────────────────────────────────────────────

class ReservationFormTest(TestCase):
    """Тесты формы ReservationForm"""

    def test_valid_form(self):
        """Корректные данные проходят валидацию"""
        form = ReservationForm(data={
            'name': 'Анна Смирнова',
            'email': 'anna@test.ru',
            'message': 'Столик на троих'
        })
        self.assertTrue(form.is_valid())

    def test_form_without_message_is_valid(self):
        """Форма валидна без сообщения"""
        form = ReservationForm(data={
            'name': 'Борис',
            'email': 'boris@test.ru',
            'message': ''
        })
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        """Невалидный email не проходит"""
        form = ReservationForm(data={
            'name': 'Тест',
            'email': 'не_email',
            'message': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_empty_name_invalid(self):
        """Пустое имя не проходит"""
        form = ReservationForm(data={
            'name': '',
            'email': 'test@test.ru',
            'message': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_form_saves_to_db(self):
        """Сохранение формы создаёт запись в БД"""
        form = ReservationForm(data={
            'name': 'Тест Сохранения',
            'email': 'save@test.ru',
            'message': 'Тест'
        })
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(Reservation.objects.filter(email='save@test.ru').count(), 1)


# ─────────────────────────────────────────────
# МОДУЛЬНЫЕ ТЕСТЫ ВЬЮХИ
# ─────────────────────────────────────────────

class ContactViewTest(TestCase):
    """Тесты вьюхи ContactView"""

    def setUp(self):
        self.client = Client()
        self.url = reverse('orders:contacts')

    def test_get_returns_200(self):
        """GET-запрос возвращает 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        """Используется шаблон orders/contacts.html"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'orders/contacts.html')

    def test_context_has_form(self):
        """Контекст содержит форму"""
        response = self.client.get(self.url)
        self.assertIn('form', response.context)

    def test_valid_post_creates_reservation(self):
        """POST с корректными данными создаёт бронирование"""
        data = {'name': 'Тест POST', 'email': 'post@test.ru', 'message': 'Привет'}
        self.client.post(self.url, data)
        self.assertTrue(Reservation.objects.filter(email='post@test.ru').exists())

    def test_valid_post_redirects(self):
        """POST перенаправляет после успеха"""
        data = {'name': 'Тест', 'email': 'r@test.ru', 'message': ''}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)

    def test_invalid_post_no_redirect(self):
        """POST с ошибками не перенаправляет"""
        response = self.client.post(self.url, {'name': '', 'email': 'bad'})
        self.assertEqual(response.status_code, 200)

    def test_success_flag_in_context(self):
        """После успешной отправки в контексте есть success=True"""
        response = self.client.get(self.url + '?ok=1')
        self.assertTrue(response.context['success'])
