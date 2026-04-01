from __future__ import annotations

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage


class OrderPage(BasePage):
    STEP_ONE_HEADER = (By.XPATH, "//div[contains(@class,'Order_Header') and normalize-space()='Для кого самокат']")
    STEP_TWO_HEADER = (By.XPATH, "//div[contains(@class,'Order_Header') and normalize-space()='Про аренду']")

    FIELD_FIRST_NAME = (By.XPATH, "//input[@placeholder='* Имя']")
    FIELD_LAST_NAME = (By.XPATH, "//input[@placeholder='* Фамилия']")
    FIELD_ADDRESS = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    FIELD_METRO = (By.XPATH, "//input[@placeholder='* Станция метро']")
    FIELD_PHONE = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
    BUTTON_NEXT = (By.XPATH, "//button[normalize-space()='Далее']")

    FIELD_DATE = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
    RENTAL_PERIOD_DROPDOWN = (By.CLASS_NAME, "Dropdown-placeholder")
    COLOR_BLACK = (By.ID, "black")
    COLOR_GREY = (By.ID, "grey")
    FIELD_COMMENT = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")
    BUTTON_CREATE_ORDER = (
        By.XPATH,
        "//div[contains(@class,'Order_Buttons')]//button[normalize-space()='Заказать']",
    )

    BUTTON_CONFIRM_ORDER = (
        By.XPATH,
        "//div[contains(@class,'Order_Modal')]//button[normalize-space()='Да']",
    )
    SUCCESS_MODAL = (By.XPATH, "//div[contains(@class,'Order_Modal')]")
    SUCCESS_HEADER = (By.XPATH, "//div[contains(@class,'Order_ModalHeader')]")
    SUCCESS_TRACK_BUTTON = (
        By.XPATH,
        "//button[contains(@class,'Button_Button') and normalize-space()='Посмотреть статус']",
    )
    SUCCESS_ORDER_NUMBER = (
        By.XPATH,
        "//div[contains(@class,'Order_Modal') and contains(., 'Номер заказа')]",
    )

    @staticmethod
    def rental_period_option(value: str) -> tuple[str, str]:
        return By.XPATH, f"//div[contains(@class,'Dropdown-option') and normalize-space()='{value}']"

    @staticmethod
    def metro_option(value: str) -> tuple[str, str]:
        return By.XPATH, (
            "//li[contains(@class,'select-search__row')]"
            f"//button[normalize-space()='{value}']"
        )

    @allure.step("Открыть страницу заказа")
    def open_order_page(self) -> OrderPage:
        self.open("/order")
        self.accept_cookies_if_present()
        return self.wait_until_loaded()

    def wait_until_loaded(self) -> OrderPage:
        self.wait_visible(self.STEP_ONE_HEADER)
        return self

    def wait_until_step_two_loaded(self) -> OrderPage:
        self.wait_visible(self.STEP_TWO_HEADER)
        return self

    @allure.step("Заполнить имя: {value}")
    def set_first_name(self, value: str) -> OrderPage:
        self.type_text(self.FIELD_FIRST_NAME, value)
        return self

    @allure.step("Заполнить фамилию: {value}")
    def set_last_name(self, value: str) -> OrderPage:
        self.type_text(self.FIELD_LAST_NAME, value)
        return self

    @allure.step("Заполнить адрес: {value}")
    def set_address(self, value: str) -> OrderPage:
        self.type_text(self.FIELD_ADDRESS, value)
        return self

    @allure.step("Выбрать станцию метро: {value}")
    def set_metro(self, value: str) -> OrderPage:
        self.type_text(self.FIELD_METRO, value)
        self.click(self.metro_option(value))
        return self

    @allure.step("Заполнить телефон: {value}")
    def set_phone(self, value: str) -> OrderPage:
        self.type_text(self.FIELD_PHONE, value)
        return self

    @allure.step("Перейти ко второму шагу заказа")
    def click_next(self) -> OrderPage:
        self.click(self.BUTTON_NEXT)
        return self.wait_until_step_two_loaded()

    @allure.step("Указать дату доставки: {value}")
    def set_delivery_date(self, value: str) -> OrderPage:
        self.type_text(self.FIELD_DATE, value)
        # Кликаем на заголовок формы, чтобы закрыть всплывающий календарь
        self.click(self.STEP_TWO_HEADER)
        return self

    @allure.step("Выбрать срок аренды: {value}")
    def set_rental_period(self, value: str) -> OrderPage:
        self.click(self.RENTAL_PERIOD_DROPDOWN)
        self.click(self.rental_period_option(value))
        return self

    @allure.step("Выбрать цвет самоката: {value}")
    def set_color(self, value: str) -> OrderPage:
        normalized = value.lower().strip()
        color_locator = self.COLOR_BLACK if normalized == 'black' else self.COLOR_GREY
        self.click(color_locator)
        return self

    @allure.step("Добавить комментарий: {value}")
    def set_comment(self, value: str) -> OrderPage:
        self.type_text(self.FIELD_COMMENT, value)
        return self

    @allure.step("Нажать кнопку 'Заказать' на шаге аренды")
    def click_create_order(self) -> OrderPage:
        self.click(self.BUTTON_CREATE_ORDER)
        return self

    @allure.step("Подтвердить оформление заказа")
    def confirm_order(self) -> OrderPage:
        self.click(self.BUTTON_CONFIRM_ORDER)
        self.wait_visible(self.SUCCESS_MODAL)
        return self

    def get_success_header_text(self) -> str:
        return self.get_text(self.SUCCESS_HEADER)

    def get_success_modal_text(self) -> str:
        return self.get_text(self.SUCCESS_MODAL)

    def get_order_number(self) -> str:
        return self.extract_order_number(self.get_text(self.SUCCESS_ORDER_NUMBER))

    def is_status_button_visible(self) -> bool:
        self.wait_visible(self.SUCCESS_TRACK_BUTTON)
        return True
