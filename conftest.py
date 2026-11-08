"""Pytest fixtures: WebDriver and page objects."""

from __future__ import annotations

import logging
from pathlib import Path

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver

load_dotenv()

from pages.base_page import BasePage
from pages.cart_page import CartPage
from pages.category_page import CategoryPage
from pages.product_page import ProductPage
from utils.allure_attach import attach_failure_artifacts
from utils.allure_env import write_environment_properties
from utils.run_config import (
    get_browser,
    get_log_level,
    is_headless,
    is_local_log,
)

logger = logging.getLogger(__name__)

DESKTOP_WIDTH, DESKTOP_HEIGHT = 1920, 1080
MOBILE_WIDTH, MOBILE_HEIGHT = 390, 844
LOG_FILE_PATH = Path("logs") / "test-run.log"


def _viewport_for(item: pytest.Item) -> tuple[int, int]:
    if item.get_closest_marker("mobile"):
        return MOBILE_WIDTH, MOBILE_HEIGHT
    return DESKTOP_WIDTH, DESKTOP_HEIGHT


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        choices=["chrome", "firefox"],
        default=None,
        help="Browser under test (overrides BROWSER env).",
    )
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Show browser window (overrides HEADLESS=true).",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Force headless mode (overrides HEADLESS=false).",
    )
    parser.addoption(
        "--local-log",
        action="store_true",
        default=False,
        help="Write logs to logs/test-run.log (overrides LOCAL_LOG).",
    )
    parser.addoption(
        "--no-local-log",
        action="store_true",
        default=False,
        help="Disable local log file even if LOCAL_LOG=true.",
    )


def pytest_configure(config):
    if config.getoption("--headed") and config.getoption("--headless"):
        raise pytest.UsageError("Use either --headed or --headless, not both.")
    if config.getoption("--local-log") and config.getoption("--no-local-log"):
        raise pytest.UsageError(
            "Use either --local-log or --no-local-log, not both."
        )

    # Fail-fast: invalid BROWSER from env/CLI before any test runs.
    try:
        get_browser(config)
        is_headless(config)
        local_log = is_local_log(config)
    except ValueError as exc:
        raise pytest.UsageError(str(exc)) from exc

    if local_log:
        LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        config.option.log_file = str(LOG_FILE_PATH)
        config.option.log_file_level = get_log_level(config)


def _build_chrome_options(
    headless: bool, width: int, height: int
) -> ChromeOptions:
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    # Quiet Chrome stderr (DevTools / GPU / GCM noise in headed runs).
    options.add_argument("--log-level=3")
    options.add_experimental_option(
        "excludeSwitches", ["enable-logging"]
    )
    options.add_argument(f"--window-size={width},{height}")
    # Capture browser console for fail-only Allure attach (independent of stderr quieting).
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    return options


def _build_firefox_options(headless: bool) -> FirefoxOptions:
    options = FirefoxOptions()
    if headless:
        options.add_argument("--headless")
    return options


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store test phase result on the item for fail-only screenshots."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture()
def driver(request):
    """Create WebDriver from BROWSER / HEADLESS (CLI overrides env)."""
    browser_name = get_browser(request.config)
    headless = is_headless(request.config)
    width, height = _viewport_for(request.node)
    my_driver: WebDriver

    logger.info(
        "browser=%s headless=%s base_url=%s viewport=%sx%s",
        browser_name,
        headless,
        BasePage.base_url,
        width,
        height,
    )

    if browser_name == "chrome":
        my_driver = webdriver.Chrome(
            options=_build_chrome_options(headless, width, height)
        )
    elif browser_name == "firefox":
        my_driver = webdriver.Firefox(
            options=_build_firefox_options(headless)
        )
        my_driver.set_window_size(width, height)
    else:
        raise ValueError(
            f"Unsupported browser: {browser_name}. "
            f"Use BROWSER=chrome or BROWSER=firefox."
        )

    if browser_name == "chrome" and not headless:
        my_driver.set_window_size(width, height)

    yield my_driver

    failed = getattr(request.node, "rep_call", None)
    if failed is not None and failed.failed:
        try:
            attach_failure_artifacts(my_driver)
        except Exception:
            logger.debug(
                "Failed to attach failure artifacts to Allure",
                exc_info=True,
            )

    my_driver.quit()


@pytest.fixture()
def cart_page(driver):
    return CartPage(driver)


@pytest.fixture()
def category_page(driver):
    return CategoryPage(driver)


@pytest.fixture()
def product_page(driver):
    return ProductPage(driver)


def pytest_sessionfinish(session, exitstatus):
    """Write Allure environment.properties after workers finish (xdist-safe)."""
    del exitstatus  # unused; required by pytest hook signature
    write_environment_properties(session.config)
