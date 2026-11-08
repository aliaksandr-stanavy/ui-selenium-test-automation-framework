from typing import Callable, Optional
from urllib.parse import urlparse

import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage
from pages.locators.cart_locators import (
    CART_EMPTY_MESSAGE,
    CART_ITEM_NAMES,
    CART_CONTINUE_SHOPPING_PAGE_BTN,
    CART_QTY_INPUT,
    CART_QTY_INCREASE,
    CART_QTY_DECREASE,
    CART_REMOVE_ITEM,
    CART_TOTAL,
    CART_CHECKOUT_BTN,
    MODAL_CONTENT,
    CART_VIEW_CART_BUTTON,
)


class CartPage(BasePage):
    page_url = '/shop/cart'

    def is_cart_empty(self) -> bool:
        return self.is_element_present(CART_EMPTY_MESSAGE)

    def get_item_names(self) -> list[str]:
        return self.get_text_list(CART_ITEM_NAMES)

    def get_item_quantity(self) -> int:
        val = self.find(CART_QTY_INPUT).get_attribute('value')
        return int(val) if val and val.isdigit() else 0

    def get_total_amount(self) -> float:
        return self.parse_price(self.get_text(CART_TOTAL))

    @staticmethod
    def _url_path(url: str) -> str:
        return urlparse(url).path.rstrip("/") or "/"

    def _click_with_retry(
            self,
            get_element: Callable[[], WebElement],
            is_done: Callable[[WebDriver], bool],
            attempts: int = 2,
            timeout: int = 8,
    ) -> None:
        """Click get_element() and wait for is_done(); retry once if needed.

        Right after landing on /shop/cart from the ATC toast, Odoo's
        quantity/remove widget JS can still be attaching its click handler
        while Selenium already considers the control clickable — a click
        that lands just before the handler is bound is a silent no-op. A
        guarded retry (skipped if is_done() already holds) resolves it
        without risking a double effect if the first click was merely slow.
        """
        last_exc: Optional[TimeoutException] = None
        for attempt in range(attempts):
            if attempt > 0 and is_done(self.driver):
                return
            element = get_element()
            self.driver.execute_script("arguments[0].click();", element)
            try:
                WebDriverWait(self.driver, timeout).until(is_done)
                return
            except TimeoutException as exc:
                last_exc = exc
        if last_exc is not None:
            raise last_exc

    @allure.step("Click Continue shopping")
    def click_continue_shopping(self):
        previous_url = self.get_current_url()
        btn = self.find_clickable(CART_CONTINUE_SHOPPING_PAGE_BTN)
        # JS click: leftover ATC toast can intercept a native click in headless.
        self.driver.execute_script("arguments[0].click();", btn)
        # `/shop` is already a substring of `/shop/cart` — require a real
        # navigation away from cart, then catalog path `/shop`.
        self.wait.until(EC.url_changes(previous_url))
        self.wait.until(lambda d: self._url_path(d.current_url) == "/shop")

    @allure.step("Reload cart page")
    def refresh(self):
        self.driver.refresh()
        self.wait.until(
            lambda d: (
                d.find_elements(*CART_ITEM_NAMES)
                or d.find_elements(*CART_EMPTY_MESSAGE)
            )
        )

    @allure.step("Open cart from 'added to cart' toast")
    def navigate_to_cart_from_modal(self):
        self.wait.until(EC.visibility_of_element_located(MODAL_CONTENT))
        view_cart_btn = self.find_clickable(CART_VIEW_CART_BUTTON)
        view_cart_btn.click()
        self.wait.until(EC.url_contains("/shop/cart"))

    @allure.step("Increase cart line quantity by one")
    def increase_item_quantity(self):
        old_qty = self.find(CART_QTY_INPUT).get_attribute('value')
        old_total = self.get_text(CART_TOTAL)
        self._click_with_retry(
            lambda: self.find_clickable(CART_QTY_INCREASE),
            lambda d: d.find_element(*CART_QTY_INPUT).get_attribute('value')
            != old_qty,
        )
        self.wait.until(
            lambda d: d.find_element(*CART_TOTAL).text.strip() != old_total
        )

    @allure.step("Decrease cart qty at 1 (stand removes the line)")
    def decrease_item_quantity_at_minimum(self):
        """Click − when qty is 1.

        Unlike the PDP qty control (clamps at 1), the cart stand removes the
        line — there is no stable cart row with quantity below 1.
        """
        self._click_with_retry(
            lambda: self.find_clickable(CART_QTY_DECREASE),
            lambda d: bool(d.find_elements(*CART_EMPTY_MESSAGE)),
        )

    @allure.step("Remove item from cart")
    def remove_item(self):
        self._click_with_retry(
            lambda: self.find_clickable(CART_REMOVE_ITEM),
            lambda d: bool(d.find_elements(*CART_EMPTY_MESSAGE)),
        )

    def verify_cart_is_empty(self):
        assert self.is_cart_empty(), "Cart is not empty, but it should be."

    def verify_item_in_cart_by_name(self, expected_name: str) -> None:
        actual_names = self.get_item_names()
        assert any(expected_name.lower() in item.lower() for item in
                   actual_names), (f"Product '{expected_name}' was not found "
                                   f"in the cart.")

    def verify_item_quantity_equals(self, expected: int) -> None:
        self.wait.until(
            lambda d: d.find_element(*CART_QTY_INPUT).get_attribute('value')
            == str(expected)
        )
        assert self.get_item_quantity() == expected, (
            f"Expected quantity {expected} in the cart, "
            f"got: {self.get_item_quantity()}"
        )

    def verify_total_increased(self, previous_total: float) -> None:
        new_total = self.get_total_amount()
        assert new_total > previous_total, (
            f"Total did not increase after qty update: "
            f"was {previous_total}, now {new_total}"
        )

    def verify_checkout_button_visible(self):
        self.verify_element_present(CART_CHECKOUT_BTN)

    def verify_checkout_button_absent(self):
        assert not self.is_element_present(CART_CHECKOUT_BTN, timeout=3), (
            "Checkout button is present on an empty cart."
        )
