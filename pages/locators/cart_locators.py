from selenium.webdriver.common.by import By

CART_ITEM_NAMES = (By.CSS_SELECTOR, "h6.fw-bold")
CART_QTY_INPUT = (By.CSS_SELECTOR, "input.js_quantity.quantity")
CART_QTY_INCREASE = (
    By.CSS_SELECTOR,
    "div[name='website_sale_cart_line_quantity'] "
    "a.js_add_cart_json[title='Add one']",
)
CART_QTY_DECREASE = (
    By.CSS_SELECTOR,
    "div[name='website_sale_cart_line_quantity'] "
    "a.js_add_cart_json[title='Remove one']",
)
CART_REMOVE_ITEM = (By.CSS_SELECTOR, "a.js_delete_product")
CART_TOTAL = (By.CSS_SELECTOR, "#order_total .oe_currency_value")
CART_CHECKOUT_BTN = (By.CSS_SELECTOR, "a[name='website_sale_main_button']")
# Post-ATC confirmation is a Bootstrap toast (not the header search modal).
MODAL_CONTENT = (By.CSS_SELECTOR, "div.toast.show")
MODAL_PRODUCT_NAME = (By.CSS_SELECTOR, "div.toast.show .toast-body span")
CART_VIEW_CART_BUTTON = (
    By.CSS_SELECTOR,
    "div.toast.show a.btn-primary[href='/shop/cart']",
)
CART_EMPTY_MESSAGE = (
    By.CSS_SELECTOR,
    "div.js_cart_lines.alert.alert-info",
)
CART_CONTINUE_SHOPPING_PAGE_BTN = (By.CSS_SELECTOR,
                                   "a[href='/shop'].text-center")
