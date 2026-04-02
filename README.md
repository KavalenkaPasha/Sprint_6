# Sprint_6 — Автотесты для Яндекс.Самокат

Автотесты на `pytest + Selenium + Firefox` для сервиса "Яндекс.Самокат"
(https://qa-scooter.praktikum-services.ru/).

---

## Что покрыто тестами

| Файл теста | Что тестируется |
|---|---|
| `tests/test_faq.py` | 8 вопросов в блоке «Вопросы о важном» — каждый отдельным тестом |
| `tests/test_order.py` | Позитивный флоу заказа: 2 Faker-сценария × 2 точки входа = 4 теста |
| `tests/test_navigation.py` | Логотип Самоката → главная; Логотип Яндекса → Дзен в новой вкладке |

---

## Структура проекта

```
Sprint_6/
├── models/
│   └── order_data.py       # dataclass OrderData, enum OrderEntryPoint
├── pages/
│   ├── base_page.py        # Базовые методы: клики, ожидания, работа с окнами
│   ├── main_page.py        # Главная страница + FAQ
│   └── order_page.py       # Форма заказа и модальное окно успеха
├── tests/
│   ├── conftest.py         # Фикстуры: driver, артефакты при падении
│   ├── data.py             # Тестовые данные FAQ и точки входа заказа
│   ├── test_faq.py         # Тесты FAQ
│   ├── test_order.py       # Тесты заказа
│   └── test_navigation.py  # Тесты навигации
├── utils/
│   └── faker_data.py       # Генерация заказов через Faker
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Установка и запуск

### 1. Создать виртуальное окружение

```bash
python -m venv venv
# venv\Scripts\activate         # Windows
```

### 2. Установить зависимости

```bash
pip install -r requirements.txt
```

### 3. Запустить тесты

```bash
# Обычный запуск (откроется браузер)
pytest

# Запуск в фоновом (headless) режиме — без GUI
pytest --headless

# Или через переменную окружения
HEADLESS=1 pytest
```

### 4. Сгенерировать и открыть Allure-отчёт

```bash
# Запустить тесты (результаты сохраняются в allure-results/)
pytest

# Открыть отчёт в браузере
allure serve allure-results

# ИЛИ собрать статический отчёт
allure generate allure-results -o allure-report --clean
allure open allure-report
```
