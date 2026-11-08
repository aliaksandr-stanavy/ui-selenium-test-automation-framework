from collections.abc import Callable
from typing import Tuple

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.remote.webdriver import WebDriver


def text_to_be_not_empty(
        locator: Tuple[str, str],
) -> Callable[[WebDriver], bool]:
    """Custom expected condition: element text is non-empty after strip."""

    def _predicate(driver: WebDriver) -> bool:
        try:
            element_text = driver.find_element(*locator).text.strip()
            return len(element_text) > 0
        except (NoSuchElementException, StaleElementReferenceException):
            return False

    return _predicate
