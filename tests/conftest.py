from __future__ import annotations

import logging
import os
import shutil
import subprocess
import sys

import allure
import pytest
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.remote.webdriver import WebDriver

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def firefox_options(pytestconfig):
    options = Options()
    headless_enabled = (
        pytestconfig.getoption("--headless") or os.getenv("HEADLESS", "0") == "1"
    )
    if headless_enabled:
        options.add_argument("--headless")

    firefox_binary = (
        os.getenv("FIREFOX_BINARY")
        or shutil.which("firefox")
        or shutil.which("firefox-esr")
    )
    if firefox_binary:
        options.binary_location = firefox_binary

    options.set_preference("dom.webnotifications.enabled", False)
    return options


def _kill_browser_processes():
    # `pkill` is available on Unix-like systems only; on Windows we skip cleanup here.
    if sys.platform.startswith("win"):
        return

    if shutil.which("pkill") is None:
        return

    for process_name in ("firefox", "geckodriver"):
        subprocess.run(
            ["pkill", "-f", process_name],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


@pytest.fixture(scope="function")
def driver(firefox_options):
    _kill_browser_processes()

    browser: WebDriver | None = None
    startup_errors: list[str] = []

    for attempt in range(2):
        try:
            browser = webdriver.Firefox(options=firefox_options)
            break
        except WebDriverException as exc:
            startup_errors.append(str(exc))
            _kill_browser_processes()
            try:
                geckodriver_path = shutil.which("geckodriver") or GeckoDriverManager().install()
                service = Service(geckodriver_path)
                browser = webdriver.Firefox(service=service, options=firefox_options)
                break
            except Exception as fallback_exc:
                startup_errors.append(str(fallback_exc))
                _kill_browser_processes()
                if attempt == 1:
                    raise RuntimeError(
                        "Не удалось запустить Firefox WebDriver. "
                        f"Причины: {' | '.join(startup_errors)}"
                    ) from fallback_exc

    if browser is None:
        raise RuntimeError("Browser not initialized")

    browser.set_window_size(1440, 1200)
    browser.set_page_load_timeout(40)

    yield browser

    try:
        while len(browser.window_handles) > 1:
            browser.switch_to.window(browser.window_handles[-1])
            browser.close()
        browser.switch_to.window(browser.window_handles[0])
    except Exception as exc:
        logger.exception("Ошибка при закрытии вкладок браузера: %s", exc)
    finally:
        try:
            browser.quit()
        except Exception as exc:
            logger.exception("Ошибка при завершении сессии браузера: %s", exc)
        _kill_browser_processes()


@pytest.hookimpl(tryfirst=True)
def pytest_addoption(parser):
    parser.addoption(
        "--headless", action="store_true", help="Запуск Firefox в headless-режиме"
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(autouse=True)
def attach_artifacts_on_failure(request):
    yield

    rep_call = getattr(request.node, "rep_call", None)
    if not (rep_call and rep_call.failed):
        return

    # Получаем driver только если он запрошен в тесте
    driver = request.node.funcargs.get("driver")
    if driver is None:
        return

    try:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="failure_screenshot",
            attachment_type=AttachmentType.PNG,
        )
    except Exception:
        allure.attach(
            "Не удалось снять скриншот: сессия браузера недоступна",
            name="failure_screenshot_error",
            attachment_type=AttachmentType.TEXT,
        )

    try:
        allure.attach(driver.current_url, name="current_url", attachment_type=AttachmentType.TEXT)
        allure.attach(driver.page_source, name="page_source", attachment_type=AttachmentType.HTML)
    except Exception:
        allure.attach(
            "Не удалось приложить URL и page source",
            name="browser_session_error",
            attachment_type=AttachmentType.TEXT,
        )

