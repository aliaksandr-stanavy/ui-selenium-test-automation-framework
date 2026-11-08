import allure
import pytest


@allure.feature("Category")
class TestCategoryPage:
    @pytest.mark.category
    @pytest.mark.smoke
    @pytest.mark.critical
    @allure.story("Product listing")
    @allure.title("Category page lists products")
    def test_products_count(self, category_page):
        category_page.open_page()
        category_page.verify_products_count_greater_than_zero()

    @pytest.mark.category
    @pytest.mark.smoke
    @pytest.mark.critical
    @allure.story("Search")
    @allure.title("Search for Desk returns matching product names")
    def test_search_desk(self, category_page):
        category_page.open_page()
        category_page.search_product("Desk")
        category_page.verify_search_results_contain_text("desk")

    @pytest.mark.category
    @pytest.mark.critical
    @allure.story("Hover add to cart")
    @allure.title("Hover add-to-cart shows matching product in modal")
    def test_hover_add_to_cart(self, category_page):
        category_page.open_page()
        p_name = category_page.add_first_product_via_hover()
        category_page.verify_modal_product_name_matches(p_name)

    @pytest.mark.category
    @pytest.mark.medium
    @allure.story("Search empty")
    @allure.title("Search with no matches shows empty state")
    def test_search_empty_results(self, category_page):
        search_query = "NonExistentItem123"
        category_page.open_page()
        category_page.search_product(search_query)

        category_page.verify_search_empty_message(search_query)
        category_page.verify_search_results_are_empty()

    @pytest.mark.category
    @pytest.mark.medium
    @pytest.mark.parametrize(
        "query,expected_substr",
        [
            ("DESK", "desk"),
            ("Des", "des"),
        ],
    )
    @allure.story("Search case and partial")
    @allure.title(
        "Search matches case-insensitive / partial query: {query}"
    )
    def test_search_case_and_partial(
            self, category_page, query, expected_substr):
        category_page.open_page()
        category_page.search_product(query)
        category_page.verify_search_results_contain_text(expected_substr)

    @pytest.mark.category
    @pytest.mark.negative
    @pytest.mark.parametrize(
        "query",
        [
            "<script>alert(1)</script>",
            "' OR '1'='1",
        ],
    )
    @allure.story("Search input resilience")
    @allure.title(
        "Malformed search input keeps UI responsive: {query}"
    )
    def test_search_resilience_malformed_input(self, category_page, query):
        """UI resilience only — not a security / XSS audit."""
        category_page.open_page()
        category_page.search_product(query)
        category_page.verify_no_js_alert()
        category_page.verify_search_remains_responsive()

    @pytest.mark.category
    @pytest.mark.medium
    @allure.story("Sort by price")
    @allure.title("Sort by price ascending orders product prices")
    def test_sort_by_price_ascending(self, category_page):
        category_page.open_page()
        category_page.sort_by_price_ascending()
        category_page.verify_prices_sorted_ascending()

    @pytest.mark.category
    @pytest.mark.regression
    @allure.story("Category to product")
    @allure.title("Product card link opens matching product detail page")
    def test_product_link_navigates_to_detail(self, category_page, product_page):
        category_page.open_page()
        name = category_page.open_first_product()
        product_page.verify_product_name_matches(name)
