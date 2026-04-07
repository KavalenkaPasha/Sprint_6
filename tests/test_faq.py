import allure
import pytest

from pages.main_page import MainPage
from pages.base_page import BasePage
from utils.test_data import FAQ_DATA


@allure.epic("Яндекс.Самокат")
@allure.feature("FAQ — Вопросы о важном")
class TestFaq:
    """
    Тесты для блока «Вопросы о важном» на главной странице.
    Каждый тест проверяет, что при клике на вопрос открывается правильный ответ.
    Параметризация позволяет запустить один тест-шаблон для всех 8 вопросов.
    """

    @allure.story("Раскрытие ответов в блоке 'Вопросы о важном'")
    @allure.title("FAQ [{question_index}]: ответ соответствует ожидаемому тексту")
    @pytest.mark.parametrize("question_index, expected_answer", FAQ_DATA)
    def test_faq_answer_matches_expected_text(self, driver, question_index, expected_answer):
        """
        Шаги:
        1. Открыть главную страницу.
        2. Прокрутить до вопроса с нужным индексом и кликнуть на него.
        3. Прочитать текст раскрывшегося ответа.
        4. Сравнить с ожидаемым значением (без учёта лишних пробелов).
        """
        with allure.step("Открыть главную страницу"): 
            main_page = MainPage(driver)
            main_page.open_main_page()

        with allure.step(f"Кликнуть на вопрос с индексом {question_index}"):
            main_page.open_faq_item(question_index)

        with allure.step("Прочитать текст ответа"):
            actual_answer = main_page.get_faq_answer_text(question_index)

        with allure.step("Сравнить полученный ответ с ожидаемым"):
            assert BasePage.normalize_text(actual_answer) == BasePage.normalize_text(expected_answer), (
                f"Для вопроса #{question_index} ожидался текст:\n«{expected_answer}»\n"
                f"Получен:\n«{actual_answer}»"
            )
