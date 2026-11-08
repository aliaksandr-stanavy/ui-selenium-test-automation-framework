import os
import re
from typing import List, Optional, Tuple
from urllib.parse import urlparse

from dotenv import load_dotenv
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.custom_expectations import text_to_be_not_empty

load_dotenv()


class BasePage:
    base_url = os.getenv("BASE_URL", "https://shop.example.com").rstrip("/")
    page_url: Optional[str] = None

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    @staticmethod
    def parse_price(text: str) -> float:
        """Parse monetary text like '$ 2,350.00' into float.

        Assumes US-style formatting (comma thousands, dot decimal),
        matching the fixed demo stand currency display.
        """
        cleaned = re.sub(r"[^\d.,]", "", text).replace(",", "")
        if not cleaned:
            raise ValueError(f"Cannot parse price from: {text!r}")
        return float(cleaned)

    def wait_until_attribute_stable(
            self,
            locator: Tuple[str, str],
            attribute: str,
            expected: str,
            timeout: int = 5,
    ) -> None:
        """Wait until attribute equals expected on two consecutive polls.

        Used when a click must not change the value (boundary), so there is
        no 'value changed' event to wait for — only post-click stability.
        """
        state: dict[str, Optional[str]] = {"prev": None}

        def _stable(driver: WebDriver) -> bool:
            val = driver.find_element(*locator).get_attribute(attribute)
            if val == expected and state["prev"] == expected:
                return True
            state["prev"] = val
            return False

        WebDriverWait(self.driver, timeout, poll_frequency=0.3).until(_stable)

    def open_page(self) -> None:
        if self.page_url is None:
            raise ValueError("Error: page_url is not defined!")
        self.driver.get(f"{self.base_url}{self.page_url}")

    def find(self, locator: Tuple[str, str]) -> WebElement:
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator: Tuple[str, str]) -> List[WebElement]:
        self.wait.until(EC.presence_of_all_elements_located(locator))
        return self.driver.find_elements(*locator)

    def get_text(self, locator: Tuple[str, str]) -> str:
        self.wait.until(text_to_be_not_empty(locator))
        return self.wait.until(
            EC.visibility_of_element_located(locator)).text.strip()

    def get_text_list(self, locator: Tuple[str, str]) -> List[str]:
        self.wait.until(EC.presence_of_all_elements_located(locator))
        return [el.text.strip() for el in self.driver.find_elements(*locator)]

    def find_clickable(self, locator: Tuple[str, str]) -> WebElement:
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element)
        return element

    def set_input_value(
            self, locator: Tuple[str, str], value: str
    ) -> WebElement:
        element = self.find_clickable(locator)
        element.clear()
        element.send_keys(value)
        element.send_keys(Keys.TAB)
        return element

    def is_element_present(self, locator: Tuple[str, str],
                           timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def scroll_to_element(self, element: WebElement) -> None:
        self.driver.execute_script("arguments[0].scrollIntoView(true);",
                                   element)

    def get_current_url(self) -> str:
        return self.driver.current_url

    def verify_url_contains(self, expected_substring: str) -> None:
        assert expected_substring in self.get_current_url(), \
            (f"URL does not match expected. Expected substring: "
             f"'{expected_substring}', actual: '{self.get_current_url()}'")

    def verify_url_path_equals(self, expected_path: str) -> None:
        """Assert URL path equals expected (ignores query/fragment)."""
        actual = urlparse(self.get_current_url()).path.rstrip("/") or "/"
        expected = expected_path.rstrip("/") or "/"
        assert actual == expected, (
            f"URL path mismatch. Expected: '{expected}', "
            f"actual: '{actual}' (full: '{self.get_current_url()}')"
        )

    def verify_text_in_element(self, locator: Tuple[str, str],
                               expected_text: str) -> None:
        actual_text = self.get_text(locator)
        assert expected_text.lower() in actual_text.lower(), \
            (f"Text '{expected_text}' not found in element. Actual "
             f"text: '{actual_text}'")

    def verify_element_present(self, locator: Tuple[str, str],
                               timeout: int = 5) -> None:
        if not self.is_element_present(locator, timeout):
            raise AssertionError(
                f"Element with locator {locator} was not found on the page.")
