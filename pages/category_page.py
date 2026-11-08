import allure
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.locators.cart_locators import MODAL_CONTENT, MODAL_PRODUCT_NAME
from pages.locators.category_locators import (
    CATEGORY_PRODUCTS,
    CATEGORY_PRODUCT_NAMES,
    CATEGORY_PRODUCT_PRICE,
    CATEGORY_CARD_NAME,
    CATEGORY_CARD_IMAGE,
    CATEGORY_CARD_ADD_TO_CART_BTN,
    CATEGORY_SEARCH_INPUT,
    CATEGORY_SEARCH_BUTTON,
    CATEGORY_SEARCH_FORM,
    SEARCH_RESULT_NAMES,
    SEARCH_EMPTY_MESSAGE,
    SORT_BY_DROPDOWN,
    SORT_DROPDOWN_TOGGLE,
    SORT_PRICE_ASC,
    CONFIG_MODAL,
    CONFIG_MODAL_CLOSE_BUTTON,
)


class CategoryPage(BasePage):
    page_url = '/shop/category/desks-1'

    def get_products_count(self) -> int:
        return len(self.find_all(CATEGORY_PRODUCTS))

    def get_product_names(self) -> list[str]:
        return self.get_text_list(CATEGORY_PRODUCT_NAMES)

    def get_product_prices(self) -> list[float]:
        texts = self.get_text_list(CATEGORY_PRODUCT_PRICE)
        return [self.parse_price(t) for t in texts]

    @allure.step("Search products: '{text}'")
    def search_product(self, text: str) -> None:
        """Fill search via JS set value + click.

        Native send_keys is flaky on this Odoo-like search widget;
        JS keeps the interaction stable across headless runs.
        """
        self.wait.until(EC.visibility_of_element_located(CATEGORY_SEARCH_FORM))
        field = self.find(CATEGORY_SEARCH_INPUT)
        self.driver.execute_script(
            "arguments[0].value = arguments[1];", field, text
        )
        search_button = self.find(CATEGORY_SEARCH_BUTTON)
        self.driver.execute_script("arguments[0].click();", search_button)
        self.wait.until(EC.url_contains("search"))

    def get_search_result_names(self) -> list[str]:
        self.wait.until(
            EC.presence_of_all_elements_located(SEARCH_RESULT_NAMES))
        return self.get_text_list(SEARCH_RESULT_NAMES)

    def _wait_toast_or_config_modal(self) -> str:
        """Return 'toast' or 'modal' once either confirmation UI is visible."""

        def _either(driver):
            toasts = driver.find_elements(*MODAL_CONTENT)
            if toasts and toasts[0].is_displayed():
                return "toast"
            modals = driver.find_elements(*CONFIG_MODAL)
            if modals and modals[0].is_displayed():
                return "modal"
            return False

        return self.wait.until(_either)

    def _dismiss_config_modal(self):
        close = self.find_clickable(CONFIG_MODAL_CLOSE_BUTTON)
        close.click()
        self.wait.until(EC.invisibility_of_element_located(CONFIG_MODAL))

    @allure.step("Add first simple product to cart via hover")
    def add_first_product_via_hover(self) -> str:
        """Hover-ATC on the first non-configurable product.

        Configurable cards (e.g. Customizable Desk) open a variant modal
        instead of the added-to-cart toast — skip those and try the next card.
        """
        products = self.find_all(CATEGORY_PRODUCTS)
        for container in products:
            product_name = container.find_element(
                *CATEGORY_CARD_NAME
            ).text.strip()
            image = container.find_element(*CATEGORY_CARD_IMAGE)

            self.scroll_to_element(image)
            ActionChains(self.driver).move_to_element(image).perform()

            cart_btn = container.find_element(*CATEGORY_CARD_ADD_TO_CART_BTN)
            self.wait.until(EC.element_to_be_clickable(cart_btn)).click()
            outcome = self._wait_toast_or_config_modal()
            if outcome == "toast":
                return product_name
            self._dismiss_config_modal()

        raise AssertionError(
            "No simple product produced an added-to-cart toast via hover ATC"
        )

    @allure.step("Sort products by price ascending")
    def sort_by_price_ascending(self):
        dropdown = self.find_clickable(SORT_BY_DROPDOWN)
        toggle = dropdown.find_element(*SORT_DROPDOWN_TOGGLE)
        toggle.click()
        option = self.find_clickable(SORT_PRICE_ASC)
        option.click()
        self.wait.until(EC.url_contains("order=list_price"))

    @allure.step("Open first product from category grid")
    def open_first_product(self) -> str:
        link = self.find_clickable(CATEGORY_PRODUCT_NAMES)
        product_name = link.text.strip()
        link.click()
        self.wait.until(lambda d: "/shop/category/" not in d.current_url)
        return product_name

    def verify_products_count_greater_than_zero(self):
        count = self.get_products_count()
        assert count > 0, f"Expected more than 0 products, got: {count}"

    def verify_search_results_contain_text(self, expected_text: str) -> None:
        names = self.get_search_result_names()
        assert len(names) > 0, "Search results are empty."
        assert all(expected_text.lower() in n.lower() for n in names), \
            f"Not all results contain '{expected_text}'"

    def verify_modal_product_name_matches(self, expected_name: str) -> None:
        modal_name = self.get_text(MODAL_PRODUCT_NAME)
        assert expected_name.lower() in modal_name.lower(), \
            (f"Modal product name ('{modal_name}') does not match expected "
             f"('{expected_name}')")

    def verify_search_empty_message(self, search_query: str) -> None:
        expected_message_text = (f"your search '{search_query}' did not match "
                                 f"anything")
        self.verify_text_in_element(SEARCH_EMPTY_MESSAGE,
                                    expected_message_text)

    def verify_search_results_are_empty(self):
        names = self.driver.find_elements(*SEARCH_RESULT_NAMES)
        assert len(names) == 0, (
            f"Expected an empty results list, but found"
            f" {len(names)} elements."
        )

    def verify_prices_sorted_ascending(self):
        prices = self.get_product_prices()
        assert len(prices) > 1, "Not enough products to verify sorting."
        assert prices == sorted(prices), (
            f"Prices are not sorted ascending: {prices}"
        )

    def verify_no_js_alert(self):
        try:
            alert = self.driver.switch_to.alert
            text = alert.text
            alert.dismiss()
            raise AssertionError(f"Unexpected JS alert: {text!r}")
        except NoAlertPresentException:
            pass

    def verify_search_remains_responsive(self):
        """UI resilience after malformed search input (not a security audit).

        Expect a normal empty-search outcome: search URL, non-empty title,
        and no product hits — without treating branded error shells as OK.
        """
        url = self.get_current_url().lower()
        assert "search" in url, (
            f"Expected search results URL after malformed input, got: "
            f"{self.get_current_url()}"
        )
        assert self.driver.title.strip(), (
            "Page title is empty after malformed search input."
        )
        self.verify_search_results_are_empty()
        self.verify_element_present(SEARCH_EMPTY_MESSAGE)
