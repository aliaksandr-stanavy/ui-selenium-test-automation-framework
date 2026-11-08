import allure
import pytest


@allure.feature("Category")
class TestMobileViewport:
    @pytest.mark.mobile
    @pytest.mark.category
    @allure.story("Mobile viewport")
    @allure.title("Category products visible on mobile viewport")
    def test_category_products_visible_on_mobile(self, category_page):
        category_page.open_page()
        category_page.verify_products_count_greater_than_zero()


@allure.feature("Product")
class TestMobileProductViewport:
    @pytest.mark.mobile
    @pytest.mark.product
    @allure.story("Mobile viewport")
    @allure.title("Product image visible on mobile viewport")
    def test_product_image_visible_on_mobile(self, product_page):
        product_page.open_page()
        product_page.verify_image_is_present()
