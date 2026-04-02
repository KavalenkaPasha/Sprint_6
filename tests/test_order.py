import allure
import pytest

from models.order_data import OrderEntryPoint
from pages.main_page import MainPage
from tests.data import ORDER_ENTRY_POINTS, ORDER_CASES
from utils.faker_data import generate_order_data



@allure.epic("Яндекс.Самокат")
@allure.feature("Заказ самоката")
class TestOrderFlow:
    """
    Тесты позитивного сценария оформления заказа самоката.

    Используется двойная параметризация:
    - entry_point: точка входа (кнопка «Заказать» сверху или снизу страницы)
    - order_data: набор тестовых данных (два разных клиента)

    Итого: 2 точки входа × 2 набора данных = 4 теста.
    """

    @allure.story("Позитивный флоу создания заказа")
    @allure.title("Заказ через точку входа [{entry_point}] и сценарий [{order_case_id}]")
    @pytest.mark.parametrize("entry_point", ORDER_ENTRY_POINTS, ids=lambda v: f"entry_{v.value}")
    @pytest.mark.parametrize("order_case_id, order_case", ORDER_CASES)
    def test_user_can_create_order_from_any_entry_point(
        self,
        driver,
        entry_point: OrderEntryPoint,
        order_case_id: str,
        order_case: dict,
    ):
        """
        Позитивный сценарий:
        1. Открыть главную страницу.
        2. Нажать кнопку «Заказать» (верхняя или нижняя — параметр entry_point).
        3. Заполнить форму — Шаг 1: личные данные + адрес + метро + телефон.
        4. Нажать «Далее» — перейти на Шаг 2.
        5. Заполнить форму — Шаг 2: дата доставки + срок аренды + цвет + комментарий.
        6. Нажать «Заказать» и подтвердить в модальном окне.
        7. Убедиться, что появилось модальное окно с сообщением об успехе.
        8. Убедиться, что в нём есть номер заказа.
        9. Убедиться, что отображается кнопка «Посмотреть статус».
        """
        with allure.step("Подготовить тестовые данные через Faker"):
            order_data = generate_order_data(case_id=order_case_id, **order_case)
            allure.attach(str(order_data), name="case_id")
            allure.attach(repr(order_data), name="generated_order_data")

        with allure.step("Открыть главную страницу"):
            main_page = MainPage(driver)
            main_page.open_main_page()

        with allure.step(f"Нажать кнопку «Заказать» — точка входа: {entry_point.value}"):
            order_page = main_page.click_order_button(entry_point)

        with allure.step("Заполнить Шаг 1: личные данные"):
            order_page.set_first_name(order_data.first_name)
            order_page.set_last_name(order_data.last_name)
            order_page.set_address(order_data.address)
            order_page.set_metro(order_data.metro)
            order_page.set_phone(order_data.phone)
            order_page.click_next()

        with allure.step("Заполнить Шаг 2: параметры аренды"):
            order_page.set_delivery_date(order_data.delivery_date)
            order_page.set_rental_period(order_data.rental_period)
            order_page.set_color(order_data.color)
            order_page.set_comment(order_data.comment)
            order_page.click_create_order()
            order_page.confirm_order()

        with allure.step("Проверить модальное окно успешного заказа"):
            success_header = order_page.get_success_header_text()
            order_number = order_page.get_order_number()

            allure.attach(success_header, name="Заголовок модального окна")
            allure.attach(order_number, name="Номер заказа")

            assert "Заказ оформлен" in success_header, (
                f"Ожидали заголовок «Заказ оформлен», но получили: «{success_header}»"
            )
            assert order_number.isdigit(), (
                f"Номер заказа должен состоять из цифр, но получено: «{order_number}»"
            )
            assert order_page.is_status_button_visible(), (
                "Кнопка «Посмотреть статус» не отображается в модальном окне"
            )
