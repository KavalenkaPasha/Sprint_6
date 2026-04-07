import allure

from pages.main_page import MainPage
from pages.order_page import OrderPage


@allure.epic("Яндекс.Самокат")
@allure.feature("Навигация по логотипам")
class TestNavigation:
    """
    Тесты навигационных элементов: логотипы «Самоката» и «Яндекса».
    Эти тесты не требуют параметризации — каждый проверяет одно конкретное поведение.
    """

    @allure.story("Логотип Самоката возвращает пользователя на главную страницу")
    @allure.title("Клик по логотипу Самоката → главная страница /")
    @allure.description(
        "Открываем страницу заказа, кликаем по логотипу «Самоката» "
        "и проверяем, что браузер перенаправил нас на главную страницу."
    )
    def test_scooter_logo_returns_user_to_home_page(self, driver):
        with allure.step("Открыть страницу заказа /order"):
            order_page = OrderPage(driver).open_order_page()

        with allure.step("Нажать на логотип Самоката"):
            main_page = order_page.click_scooter_logo()

        with allure.step("Проверить, что открылась главная страница"):
            expected_url = MainPage.build_url("/")
            actual_url = main_page.current_url()

            allure.attach(actual_url, name="Текущий URL после клика")
            allure.attach(expected_url, name="Ожидаемый URL")

            assert actual_url == expected_url, (
                f"Ожидался URL: «{expected_url}», получен: «{actual_url}»"
            )
            assert main_page.is_loaded(), (
                "Главная страница не загрузилась после клика по логотипу Самоката"
            )

    @allure.story("Логотип Яндекса открывает Дзен в новой вкладке")
    @allure.title("Клик по логотипу Яндекса → новая вкладка с dzen.ru")
    @allure.description(
        "Кликаем на логотип Яндекса на главной странице. "
        "Ожидаем, что откроется новая вкладка и после редиректа "
        "там окажется страница Дзена (dzen.ru)."
    )
    def test_yandex_logo_opens_dzen_in_new_tab(self, driver):
        with allure.step("Открыть главную страницу"):
            main_page = MainPage(driver).open_main_page()

        with allure.step("Запомнить текущую вкладку и список всех открытых вкладок"):
            original_handle = driver.current_window_handle
            existing_handles = driver.window_handles.copy()

        with allure.step("Нажать на логотип Яндекса"):
            main_page.click_yandex_logo()

        with allure.step("Переключиться на новую вкладку"):
            dzen_handle = main_page.wait_for_new_window(existing_handles)
            main_page.switch_to_window(dzen_handle)

        with allure.step("Дождаться загрузки страницы Дзена"):
            main_page.wait_url_contains("dzen.ru", timeout=20)
            main_page.wait_title_not_empty(timeout=20)

        with allure.step("Проверить, что открылась страница Дзена"):
            current_url = driver.current_url
            current_title = driver.title.strip()

            allure.attach(current_url, name="URL новой вкладки")
            allure.attach(current_title, name="Title новой вкладки")

            assert "dzen.ru" in current_url, (
                f"Ожидали URL с «dzen.ru», но получили: «{current_url}»"
            )
            assert current_title, "Страница Дзена загрузилась, но у неё пустой заголовок (title)"

        with allure.step("Закрыть вкладку Дзена и вернуться на исходную"):
            main_page.close_current_tab_and_switch_back(original_handle)
            assert driver.current_window_handle == original_handle, (
                "Не удалось вернуться в исходную вкладку после закрытия вкладки Дзена"
            )
