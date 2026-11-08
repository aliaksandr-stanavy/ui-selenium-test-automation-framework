import allure
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.locators.cart_locators import MODAL_CONTENT
from pages.locators.product_locators import (
    PRODUCT_IMAGE,
    PRODUCT_NAME,
    PRODUCT_PRICE,
    PRODUCT_QUANTITY_INPUT,
    PRODUCT_INCREASE_QUANTITY,
    PRODUCT_DECREASE_QUANTITY,
    PRODUCT_ADD_TO_CART_BUTTON,
    PRODUCT_BREADCRUMB,
    PRODUCT_TERMS_BLOCK,
)


class ProductPage(BasePage):
    page_url = '/shop/furn-9999-office-design-software-7'

    def open_with_category(self, category_id: int) -> None:
        self.driver.get(
            f"{self.base_url}{self.page_url}?category={category_id}"
        )

    def is_image_present(self) -> bool:
        return self.is_element_present(PRODUCT_IMAGE)

    def get_product_name(self) -> str:
        return self.get_text(PRODUCT_NAME)

    def get_quantity(self) -> int:
        val = self.find(PRODUCT_QUANTITY_INPUT).get_attribute('value')
        return int(val) if val and val.isdigit() else 0

    def get_quantity_raw(self) -> str:
        return self.find(PRODUCT_QUANTITY_INPUT).get_attribute('value') or ''

    @allure.step("Change quantity (increase={increase})")
    def change_quantity(self, increase: bool = True) -> None:
        old_val = self.find(PRODUCT_QUANTITY_INPUT).get_attribute('value')
        locator = (
            PRODUCT_INCREASE_QUANTITY if increase else PRODUCT_DECREASE_QUANTITY
        )

        btn = self.find_clickable(locator)
        btn.click()

        self.wait.until(
            lambda d: d.find_element(*PRODUCT_QUANTITY_INPUT).get_attribute(
                'value') != old_val)

    @allure.step("Click decrease at minimum quantity (expect no change)")
    def decrease_quantity_at_minimum(self):
        """Click decrease; qty must remain 1 after a stable post-click read."""
        expected = self.find(PRODUCT_QUANTITY_INPUT).get_attribute('value')
        btn = self.find_clickable(PRODUCT_DECREASE_QUANTITY)
        btn.click()
        self.wait_until_attribute_stable(
            PRODUCT_QUANTITY_INPUT, "value", expected or "1"
        )

    @allure.step("Set quantity via direct input: {value}")
    def set_quantity_via_input(self, value: str) -> None:
        self.set_input_value(PRODUCT_QUANTITY_INPUT, value)

    @allure.step("Recover quantity via increase control after invalid input")
    def recover_quantity_via_increase(self):
        """Click + after invalid direct input; UI restores a numeric qty."""
        self.change_quantity(increase=True)

    @allure.step("Add product to cart from details page")
    def add_to_cart(self):
        btn = self.find_clickable(PRODUCT_ADD_TO_CART_BUTTON)
        btn.click()
        self.wait.until(EC.visibility_of_element_located(MODAL_CONTENT))

    def verify_image_is_present(self):
        assert self.is_image_present(), "Product image was not found."

    def verify_price_is_displayed(self):
        text = self.get_text(PRODUCT_PRICE)
        price = self.parse_price(text)
        assert price > 0, f"Expected a positive price, got: {text}"

    def verify_quantity_is_one(self):
        current_qty = self.get_quantity()
        assert current_qty == 1, (f"Expected quantity 1, got:"
                                  f" {current_qty}")

    def verify_quantity_did_not_change(self):
        new_qty = self.get_quantity()
        assert new_qty == 1, (f"Quantity changed to {new_qty}, "
                              f"but it should have stayed 1.")

    def verify_quantity_is_two(self):
        self.wait.until(
            EC.text_to_be_present_in_element_value(PRODUCT_QUANTITY_INPUT,
                                                   "2"))
        qty = self.find(PRODUCT_QUANTITY_INPUT).get_attribute('value')
        assert qty == "2", f"Expected quantity 2, got: {qty}"

    def verify_quantity_equals(self, expected: int) -> None:
        self.wait.until(
            lambda d: d.find_element(*PRODUCT_QUANTITY_INPUT).get_attribute(
                'value') == str(expected)
        )
        assert self.get_quantity() == expected, (
            f"Expected quantity {expected}, got: {self.get_quantity()}"
        )

    def verify_quantity_is_positive_integer(self):
        raw = self.get_quantity_raw().strip()
        assert raw.isdigit() and int(raw) >= 1, (
            f"Expected a valid positive integer quantity, "
            f"got: {raw!r}"
        )

    def verify_modal_is_present(self):
        self.verify_element_present(MODAL_CONTENT)

    def verify_product_name_matches(self, expected_name: str) -> None:
        actual = self.get_product_name()
        assert expected_name.lower() in actual.lower(), (
            f"PDP name ('{actual}') does not match the card "
            f"('{expected_name}')"
        )

    def verify_terms_and_conditions_visible(self):
        self.verify_element_present(PRODUCT_TERMS_BLOCK)
        self.verify_text_in_element(PRODUCT_TERMS_BLOCK, "Terms and Conditions")

    def verify_breadcrumb_contains(self, expected_text: str) -> None:
        self.verify_text_in_element(PRODUCT_BREADCRUMB, expected_text)
