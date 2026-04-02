from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING, Iterable

import allure
from allure_commons.types import AttachmentType
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

if TYPE_CHECKING:
    from selenium.webdriver.firefox.webdriver import WebDriver


logger = logging.getLogger(__name__)


class BasePage:
    BASE_URL = "https://qa-scooter.praktikum-services.ru"
    DEFAULT_TIMEOUT = 15
    ORDER_NUMBER_PATTERN = re.compile(r"Номер заказа[:\s№]*(\d+)")

    SCOOTER_LOGO = (By.CSS_SELECTOR, "a[href='/']")
    YANDEX_LOGO = (By.CSS_SELECTOR, "a[href*='yandex.ru']")
    COOKIE_BUTTON = (By.ID, "rcc-confirm-button")
    COOKIE_BUTTON_FALLBACK = (By.XPATH, "//button[contains(., 'да все привыкли')]")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)

    @staticmethod
    def build_url(path: str = "") -> str:
        return f"{BasePage.BASE_URL}{path}"

    @allure.step("Открыть страницу: {path}")
    def open(self, path: str = "") -> BasePage:
        self.driver.get(self.build_url(path))
        return self

    def wait_visible(self, locator: tuple[str, str], timeout: int | None = None) -> WebElement:
        return WebDriverWait(self.driver, timeout or self.DEFAULT_TIMEOUT).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_present(self, locator: tuple[str, str], timeout: int | None = None) -> WebElement:
        return WebDriverWait(self.driver, timeout or self.DEFAULT_TIMEOUT).until(
            EC.presence_of_element_located(locator)
        )

    def wait_clickable(self, locator: tuple[str, str], timeout: int | None = None) -> WebElement:
        return WebDriverWait(self.driver, timeout or self.DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_all_present(self, locator: tuple[str, str], timeout: int | None = None) -> list[WebElement]:
        WebDriverWait(self.driver, timeout or self.DEFAULT_TIMEOUT).until(
            EC.presence_of_all_elements_located(locator)
        )
        return self.driver.find_elements(*locator)

    @allure.step("Прокрутить страницу к элементу")
    def scroll_to(self, locator: tuple[str, str]) -> WebElement:
        element = self.wait_present(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            element,
        )
        return element

    @allure.step("Кликнуть по элементу")
    def click(self, locator: tuple[str, str], *, scroll: bool = False, timeout: int | None = None) -> WebElement:
        if scroll:
            self.scroll_to(locator)
        element = self.wait_clickable(locator, timeout)
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)
        return element

    @allure.step("Заполнить поле значением: {value}")
    def type_text(
        self,
        locator: tuple[str, str],
        value: str,
        *,
        clear: bool = True,
        scroll: bool = False,
    ) -> WebElement:
        if scroll:
            self.scroll_to(locator)
        element = self.wait_visible(locator)
        if clear:
            element.clear()
        element.send_keys(value)
        return element

    def get_text(self, locator: tuple[str, str], timeout: int | None = None) -> str:
        return self.wait_visible(locator, timeout).text

    def wait_url_contains(self, value: str, timeout: int | None = None) -> bool:
        return WebDriverWait(self.driver, timeout or self.DEFAULT_TIMEOUT).until(EC.url_contains(value))

    def wait_url_to_be(self, value: str, timeout: int | None = None) -> bool:
        return WebDriverWait(self.driver, timeout or self.DEFAULT_TIMEOUT).until(EC.url_to_be(value))

    def wait_title_not_empty(self, timeout: int | None = None) -> bool:
        return WebDriverWait(self.driver, timeout or self.DEFAULT_TIMEOUT).until(lambda d: d.title.strip() != "")

    def current_url(self) -> str:
        return self.driver.current_url

    def current_title(self) -> str:
        return self.driver.title

    @staticmethod
    def normalize_text(value: str) -> str:
        return " ".join(value.split())

    @allure.step("Принять cookies, если баннер отображается")
    def accept_cookies_if_present(self) -> BasePage:
        for locator in (self.COOKIE_BUTTON, self.COOKIE_BUTTON_FALLBACK):
            try:
                self.click(locator, timeout=3)
                break
            except TimeoutException:
                continue
        return self

    @allure.step("Открыть главную страницу по логотипу Самоката")
    def click_scooter_logo(self):
        self.click(self.SCOOTER_LOGO)
        from pages.main_page import MainPage

        return MainPage(self.driver)

    @allure.step("Нажать на логотип Яндекса")
    def click_yandex_logo(self) -> BasePage:
        self.click(self.YANDEX_LOGO)
        return self

    def wait_for_new_window(self, existing_handles: Iterable[str], timeout: int | None = None) -> str:
        existing_handles = list(existing_handles)
        WebDriverWait(self.driver, timeout or self.DEFAULT_TIMEOUT).until(
            lambda d: len(d.window_handles) > len(existing_handles)
        )
        new_handles = [handle for handle in self.driver.window_handles if handle not in existing_handles]
        return new_handles[-1]

    @allure.step("Переключиться на вкладку")
    def switch_to_window(self, handle: str) -> BasePage:
        self.driver.switch_to.window(handle)
        return self

    @allure.step("Закрыть текущую вкладку и вернуться обратно")
    def close_current_tab_and_switch_back(self, target_handle: str) -> BasePage:
        if len(self.driver.window_handles) > 1:
            self.driver.close()
        self.driver.switch_to.window(target_handle)
        return self

    def extract_order_number(self, value: str) -> str:
        normalized_value = self.normalize_text(value)
        match = self.ORDER_NUMBER_PATTERN.search(normalized_value)
        if not match:
            raise AssertionError(
                f"Не удалось извлечь номер заказа из текста модального окна: «{normalized_value}»"
            )
        return match.group(1)

    def attach_screenshot(self, name: str = "screenshot") -> None:
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=AttachmentType.PNG,
        )

    def attach_text(self, name: str, value: str) -> None:
        allure.attach(value, name=name, attachment_type=AttachmentType.TEXT)
