from selenium.webdriver.common.by import By

CATEGORY_PRODUCTS = (By.CSS_SELECTOR, "td.oe_product")
# Page-scoped (driver.find_*).
CATEGORY_PRODUCT_NAMES = (By.CSS_SELECTOR, "a[itemprop='name']")
CATEGORY_PRODUCT_PRICE = (
    By.CSS_SELECTOR,
    "td.oe_product .product_price .oe_currency_value",
)
# Card-scoped (element.find_*): relative to CATEGORY_PRODUCTS container.
# Do not repeat `td.oe_product` — Selenium searches descendants only.
CATEGORY_CARD_NAME = (By.CSS_SELECTOR, "a[itemprop='name']")
CATEGORY_CARD_IMAGE = (
    By.CSS_SELECTOR,
    ".oe_product_image_img_wrapper img",
)
CATEGORY_CARD_ADD_TO_CART_BTN = (
    By.CSS_SELECTOR,
    ".btn.btn-primary.a-submit",
)
CATEGORY_SEARCH_INPUT = (By.CSS_SELECTOR, "input.search-query")
CATEGORY_SEARCH_BUTTON = (By.CSS_SELECTOR, "button.oe_search_button")
CATEGORY_SEARCH_FORM = (
    By.CSS_SELECTOR,
    "form.o_wsale_products_searchbar_form",
)
SEARCH_RESULT_NAMES = (By.CSS_SELECTOR, "a.dropdown-item div.h6.fw-bold")
SEARCH_EMPTY_MESSAGE = (
    By.XPATH,
    "//div[contains(@class,'alert') and contains(., 'did not match')]",
)
SORT_BY_DROPDOWN = (By.CSS_SELECTOR, "div.o_sortby_dropdown")
SORT_DROPDOWN_TOGGLE = (By.CSS_SELECTOR, "a.dropdown-toggle")
SORT_PRICE_ASC = (
    By.CSS_SELECTOR,
    "div.o_sortby_dropdown a.dropdown-item[href*='order=list_price+asc']",
)
CONFIG_MODAL = (By.CSS_SELECTOR, "div.modal.show")
CONFIG_MODAL_CLOSE_BUTTON = (
    By.CSS_SELECTOR,
    "div.modal.show button.btn-close",
)
