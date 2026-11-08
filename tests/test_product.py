import allure
import pytest

# Product under test belongs to Multimedia (category id=9) on the demo stand.
# See docs/en/brd.md — breadcrumb shows category only with ?category=<id>.
MULTIMEDIA_CATEGORY_ID = 9
MULTIMEDIA_CATEGORY_NAME = "Multimedia"


@allure.feature("Product")
class TestProductPage:
    @pytest.mark.product
    @pytest.mark.smoke
    @pytest.mark.critical
    @allure.story("Product image")
    @allure.title("Product detail image is visible")
    def test_image_visible(self, product_page):
        product_page.open_page()
        product_page.verify_image_is_present()

    @pytest.mark.product
    @pytest.mark.medium
    @allure.story("Quantity boundaries")
    @allure.title("Quantity does not go below 1")
    def test_quantity_limits(self, product_page):
        product_page.open_page()
        product_page.verify_quantity_is_one()
        product_page.decrease_quantity_at_minimum()
        product_page.verify_quantity_did_not_change()

    @pytest.mark.product
    @pytest.mark.medium
    @allure.story("Quantity control")
    @allure.title("Increase quantity sets value to 2")
    def test_quantity_control(self, product_page):
        product_page.open_page()
        product_page.change_quantity(increase=True)
        product_page.verify_quantity_is_two()

    @pytest.mark.product
    @pytest.mark.smoke
    @pytest.mark.critical
    @allure.story("Add to cart")
    @allure.title("Add from product details opens confirmation modal")
    def test_add_from_details(self, product_page):
        product_page.open_page()
        product_page.add_to_cart()
        product_page.verify_modal_is_present()

    @pytest.mark.product
    @pytest.mark.smoke
    @allure.story("Product price")
    @allure.title("Product price is displayed on detail page")
    def test_price_is_displayed(self, product_page):
        product_page.open_page()
        product_page.verify_price_is_displayed()

    @pytest.mark.product
    @pytest.mark.medium
    @allure.story("Quantity direct input")
    @allure.title("Direct quantity input accepts valid value 3")
    def test_quantity_direct_input_valid(self, product_page):
        product_page.open_page()
        product_page.set_quantity_via_input("3")
        product_page.verify_quantity_equals(3)

    @pytest.mark.product
    @pytest.mark.negative
    @pytest.mark.parametrize("value", ["0", "abc"])
    @allure.story("Quantity invalid input")
    @allure.title(
        "Invalid quantity input is recoverable to a positive integer: {value}"
    )
    def test_quantity_direct_input_invalid(self, product_page, value):
        product_page.open_page()
        product_page.set_quantity_via_input(value)
        product_page.recover_quantity_via_increase()
        product_page.verify_quantity_is_positive_integer()

    @pytest.mark.product
    @pytest.mark.medium
    @allure.story("Breadcrumb")
    @allure.title(
        "Breadcrumb contains category Multimedia when opened with category"
    )
    def test_breadcrumb_contains_category(self, product_page):
        product_page.open_with_category(MULTIMEDIA_CATEGORY_ID)
        product_page.verify_breadcrumb_contains(MULTIMEDIA_CATEGORY_NAME)

    @pytest.mark.product
    @pytest.mark.smoke
    @allure.story("Terms")
    @allure.title("Terms and Conditions block is visible")
    def test_terms_and_conditions_visible(self, product_page):
        product_page.open_page()
        product_page.verify_terms_and_conditions_visible()
