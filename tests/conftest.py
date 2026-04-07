import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    browser = webdriver.Firefox()
    browser.set_window_size(1440, 1200)
    browser.set_page_load_timeout(40)
    yield browser
    browser.quit()
