from __future__ import annotations

import allure
from selenium.webdriver.common.by import By

from models.order_data import OrderEntryPoint
from pages.base_page import BasePage


class MainPage(BasePage):
    ORDER_BUTTON_TOP = (
        By.XPATH,
        "//div[contains(@class,'Header_Nav')]//button[normalize-space()='Заказать']",
    )
    ORDER_BUTTON_BOTTOM = (
        By.XPATH,
        "//div[contains(@class,'Home_FinishButton')]//button[normalize-space()='Заказать']",
    )

    @staticmethod
    def faq_question(index: int) -> tuple[str, str]:
        return By.ID, f"accordion__heading-{index}"

    @staticmethod
    def faq_answer(index: int) -> tuple[str, str]:
        return By.ID, f"accordion__panel-{index}"

    @allure.step("Открыть главную страницу Самоката")
    def open_main_page(self) -> MainPage:
        self.open("/")
        self.accept_cookies_if_present()
        self.wait_visible(self.ORDER_BUTTON_TOP)
        return self

    @allure.step("Нажать кнопку заказа: {entry_point}")
    def click_order_button(self, entry_point: OrderEntryPoint):
        from pages.order_page import OrderPage

        if entry_point is OrderEntryPoint.TOP:
            self.click(self.ORDER_BUTTON_TOP)
        else:
            self.click(self.ORDER_BUTTON_BOTTOM, scroll=True)
        order_page = OrderPage(self.driver)
        order_page.wait_until_loaded()
        return order_page

    @allure.step("Раскрыть вопрос FAQ с индексом {index}")
    def open_faq_item(self, index: int) -> MainPage:
        locator = self.faq_question(index)
        self.click(locator, scroll=True)
        return self

    @allure.step("Получить текст ответа FAQ с индексом {index}")
    def get_faq_answer_text(self, index: int) -> str:
        return self.get_text(self.faq_answer(index))

    def is_loaded(self) -> bool:
        self.wait_visible(self.ORDER_BUTTON_TOP)
        return True
