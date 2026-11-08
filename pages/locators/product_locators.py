from selenium.webdriver.common.by import By

PRODUCT_NAME = (By.CSS_SELECTOR, "h1[itemprop='name']")
PRODUCT_IMAGE = (By.CSS_SELECTOR, 'img.product_detail_img')
PRODUCT_PRICE = (By.CSS_SELECTOR, 'span.oe_price .oe_currency_value')
PRODUCT_ADD_TO_CART_BUTTON = (By.ID, 'add_to_cart')
PRODUCT_QUANTITY_INPUT = (By.CSS_SELECTOR, 'input.quantity')
PRODUCT_INCREASE_QUANTITY = (By.CSS_SELECTOR,
                             "a.js_add_cart_json[title='Add one']")
PRODUCT_DECREASE_QUANTITY = (By.CSS_SELECTOR,
                             "a.js_add_cart_json[title='Remove one']")
PRODUCT_BREADCRUMB = (By.CSS_SELECTOR, 'ol.breadcrumb')
PRODUCT_TERMS_BLOCK = (By.ID, 'o_product_terms_and_share')
