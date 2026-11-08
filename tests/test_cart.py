import allure
import pytest


def _add_one_item_and_open_cart(product_page, cart_page):
    """Shared setup: open PDP, add to cart, open cart from modal."""
    product_page.open_page()
    product_page.add_to_cart()
    cart_page.navigate_to_cart_from_modal()


@allure.feature("Cart")
class TestCartPage:
    @pytest.mark.cart
    @pytest.mark.smoke
    @pytest.mark.critical
    @allure.story("Empty cart")
    @allure.title("Empty cart shows empty-state message")
    def test_empty_cart(self, cart_page):
        cart_page.open_page()
        cart_page.verify_cart_is_empty()

    @pytest.mark.cart
    @pytest.mark.critical
    @allure.story("Add to cart")
    @allure.title("Product name appears in cart after add via modal")
    def test_item_in_cart(self, product_page, cart_page):
        product_page.open_page()
        expected_name = product_page.get_product_name()
        product_page.add_to_cart()
        cart_page.navigate_to_cart_from_modal()
        cart_page.verify_item_in_cart_by_name(expected_name)

    @pytest.mark.cart
    @pytest.mark.medium
    @allure.story("Continue shopping")
    @allure.title("Continue shopping returns to shop catalog")
    def test_continue_shopping(self, product_page, cart_page):
        _add_one_item_and_open_cart(product_page, cart_page)
        cart_page.click_continue_shopping()
        cart_page.verify_url_path_equals("/shop")

    @pytest.mark.cart
    @pytest.mark.critical
    @allure.story("Modal navigation")
    @allure.title("View cart from modal opens /shop/cart URL")
    def test_cart_navigation_via_modal(self, product_page, cart_page):
        _add_one_item_and_open_cart(product_page, cart_page)
        cart_page.verify_url_contains("/shop/cart")

    @pytest.mark.cart
    @pytest.mark.critical
    @allure.story("Cart quantity and total")
    @allure.title("Increasing cart quantity recalculates total")
    def test_cart_update_quantity_recalculates_total(
            self, product_page, cart_page):
        _add_one_item_and_open_cart(product_page, cart_page)
        previous_total = cart_page.get_total_amount()
        cart_page.increase_item_quantity()
        cart_page.verify_item_quantity_equals(2)
        cart_page.verify_total_increased(previous_total)

    @pytest.mark.cart
    @pytest.mark.medium
    @allure.story("Cart quantity boundaries")
    @allure.title("Decreasing cart quantity at 1 removes the line")
    def test_cart_quantity_does_not_go_below_one(
            self, product_page, cart_page):
        """Cart cannot keep a line with qty < 1: − at 1 clears the cart."""
        _add_one_item_and_open_cart(product_page, cart_page)
        cart_page.verify_item_quantity_equals(1)
        cart_page.decrease_item_quantity_at_minimum()
        cart_page.verify_cart_is_empty()

    @pytest.mark.cart
    @pytest.mark.critical
    @allure.story("Remove from cart")
    @allure.title("Removing item returns cart to empty state")
    def test_cart_remove_item_returns_to_empty(self, product_page, cart_page):
        _add_one_item_and_open_cart(product_page, cart_page)
        cart_page.remove_item()
        cart_page.verify_cart_is_empty()

    @pytest.mark.cart
    @pytest.mark.smoke
    @allure.story("Checkout CTA")
    @allure.title("Checkout button is visible when cart has items")
    def test_checkout_visible_when_items(self, product_page, cart_page):
        _add_one_item_and_open_cart(product_page, cart_page)
        cart_page.verify_checkout_button_visible()

    @pytest.mark.cart
    @pytest.mark.negative
    @allure.story("Checkout CTA")
    @allure.title("Checkout button is absent on empty cart")
    def test_checkout_absent_when_empty(self, cart_page):
        cart_page.open_page()
        cart_page.verify_checkout_button_absent()

    @pytest.mark.cart
    @pytest.mark.regression
    @allure.story("Cart persistence")
    @allure.title("Cart item persists after page reload")
    def test_cart_persists_after_reload(self, product_page, cart_page):
        product_page.open_page()
        expected_name = product_page.get_product_name()
        product_page.add_to_cart()
        cart_page.navigate_to_cart_from_modal()
        cart_page.refresh()
        cart_page.verify_item_in_cart_by_name(expected_name)

    @pytest.mark.cart
    @pytest.mark.regression
    @allure.story("Quantity passthrough")
    @allure.title("Quantity selected on product page is reflected in cart")
    def test_qty_from_product_reflected_in_cart(self, product_page, cart_page):
        product_page.open_page()
        product_page.set_quantity_via_input("3")
        product_page.verify_quantity_equals(3)
        product_page.add_to_cart()
        cart_page.navigate_to_cart_from_modal()
        cart_page.verify_item_quantity_equals(3)
