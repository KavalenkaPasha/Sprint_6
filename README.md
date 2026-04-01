# Sprint_6 — Автотесты для Яндекс.Самокат

Автотесты на `pytest + Selenium + Firefox` для учебного сервиса **Яндекс.Самокат**
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

## Стек технологий

- **Python 3.10+**
- **pytest** — фреймворк для тестов
- **Selenium 4** — управление браузером
- **Mozilla Firefox** + **geckodriver** (через webdriver-manager)
- **Allure** — генерация красивых отчётов
- **Faker** — генерация реалистичных и частично детерминированных тестовых данных

---

## Установка и запуск

### 1. Создать виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows
```

### 2. Установить зависимости

```bash
pip install -r requirements.txt
```

> **Требования**: Mozilla Firefox должен быть установлен.  
> `geckodriver` скачивается автоматически через `webdriver-manager`.

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

---

## Параметризация

### FAQ — 8 параметров

```python
@pytest.mark.parametrize("question_index, expected_answer", FAQ_DATA)
```

Один тест-шаблон × 8 элементов `FAQ_DATA` = **8 тестов**.

### Заказ — 2×2 параметры

```python
@pytest.mark.parametrize("entry_point", ORDER_ENTRY_POINTS)          # TOP, BOTTOM
@pytest.mark.parametrize("order_case_id, order_case", ORDER_CASES)  # 2 Faker-сценария
```

Декартово произведение: 2 × 2 = **4 теста**.

Для заказов используется `utils/faker_data.py`: случайными остаются имя, фамилия, адрес и телефон, а стабильными — метро, срок аренды, цвет и смещения даты доставки. Это делает данные реалистичнее без потери повторяемости.

---

## Артефакты при падении

При падении любого теста в Allure автоматически прикрепляются:
- 📸 Скриншот браузера
- 🔗 Текущий URL
- 📄 HTML-код страницы
