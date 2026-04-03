# Sprint_6 — автотесты для Яндекс.Самокат

Автотесты на `pytest + Selenium + Firefox` для сервиса «Яндекс.Самокат»:
https://qa-scooter.praktikum-services.ru/

## Что покрыто тестами

- `tests/test_faq.py` — блок «Вопросы о важном», отдельный тест на каждый вопрос через параметризацию.
- `tests/test_order.py` — позитивный сценарий оформления заказа с двумя наборами данных и двумя точками входа.
- `tests/test_navigation.py` — переход по логотипу «Самоката» на главную страницу и открытие Дзена по логотипу Яндекса.

## Структура проекта

```text
Sprint_6/
├── models/
│   └── order_data.py
├── pages/
│   ├── base_page.py
│   ├── main_page.py
│   └── order_page.py
├── tests/
│   ├── conftest.py
│   ├── test_faq.py
│   ├── test_order.py
│   └── test_navigation.py
├── utils/
│   ├── faker_data.py
│   └── test_data.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## Установка и запуск

### 1. Создать виртуальное окружение

```bash
python -m venv venv
# source venv/bin/activate
# или venv\Scripts\activate для Windows
```

### 2. Установить зависимости

```bash
pip install -r requirements.txt
```

### 3. Запустить тесты

```bash
pytest
```

### 4. Сгенерировать Allure-отчёт

```bash
allure serve allure-results
```

или:

```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```
