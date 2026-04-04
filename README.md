# B&B COFFEE — Django-сайт кофейни
Учебная практика УП.04.01 | РКСИ | Специальность 09.02.07

## Быстрый старт

```bash
# 1. Распаковать архив и перейти в папку
unzip bb_coffee_project.zip && cd bb_coffee_project

# 2. Создать виртуальное окружение
python -m venv venv
source venv/bin/activate          # Linux/Mac
venv\Scripts\activate             # Windows

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Применить миграции
python manage.py migrate

# 5. Заполнить БД меню и создать суперпользователя
python manage.py seed_menu

# 6. Запустить сервер
python manage.py runserver
```

Сайт:       http://127.0.0.1:8000  
Меню:       http://127.0.0.1:8000/menu/  
Контакты:   http://127.0.0.1:8000/orders/contacts/  
Админ:      http://127.0.0.1:8000/admin/  
Логин: Admin | Пароль: admin123

## Запуск тестов

```bash
# Все тесты (57 штук)
python manage.py test menu pages orders tests_integration --verbosity=2

# Только модульные
python manage.py test menu pages orders

# Только интеграционные
python manage.py test tests_integration
```

## Структура проекта

```
bb_coffee/          — настройки Django
menu/               — приложение: категории и позиции меню
  models.py         — Category, MenuItem
  views.py          — MenuView (CBV)
  admin.py          — регистрация в админке
  tests.py          — модульные тесты (ПР №12)
  management/commands/seed_menu.py — заполнение БД
orders/             — приложение: бронирование столиков
  models.py         — Reservation
  forms.py          — ReservationForm
  views.py          — ContactView (CBV)
  admin.py
  tests.py          — модульные тесты (ПР №12)
pages/              — главная страница
  tests.py          — модульные тесты (ПР №12)
tests_integration.py — интеграционные тесты (ПР №13)
templates/          — HTML-шаблоны (base.html + 3 страницы)
static/css/         — main.css (CSS-переменные, без Bootstrap)
static/js/          — main.js (мобильное меню, скролл, анимации)
```

## Меню (35 позиций, 5 категорий)

| Категория         | Позиций |
|-------------------|---------|
| Кофе              | 12      |
| Авторские напитки | 5       |
| Чай и напитки     | 6       |
| Десерты           | 7       |
| Завтраки          | 5       |

## Соответствие ТЗ

| Пункт ТЗ | Реализация |
|----------|-----------|
| ПР №3  Техническое задание      | Настоящий README |
| ПР №5  Проектирование интерфейса | Макеты воспроизведены, адаптив |
| ПР №7  Проектирование БД        | SQLite, 3 модели, миграции |
| ПР №10 Backend-модули           | 3 Django-приложения, CBV |
| ПР №11 Административная панель  | Django Admin, кастомные list_display |
| ПР №12 Модульное тестирование   | 37 unit-тестов (models, views, forms) |
| ПР №13 Интеграционное тестирование | 20 интеграционных тестов |
| ПР №14 Анализ рисков            | SecurityTest: CSRF, XSS, auth |
| ПР №15 Безопасность backend     | CSRF middleware, экранирование шаблонов |
