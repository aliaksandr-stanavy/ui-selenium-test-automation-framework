# Fixtures reference

Available fixtures and when to use them.

**Language:** English · [Русский](../ru/fixtures-reference.md)

Architecture: [`architecture.md`](architecture.md). Scenario map: [`qa-requirements.md`](qa-requirements.md).

---

## `driver`

| | |
|--|--|
| Scope | function |
| Purpose | WebDriver (Chrome / Firefox); **1920×1080** by default, **390×844** for `@pytest.mark.mobile` |
| Env / CLI | `BROWSER` / `--browser`; `HEADLESS` / `--headed`/`--headless`; `LOCAL_LOG` / `--local-log` |
| Default | `chrome`, headless=`true`, local log=`false` |
| Teardown | on failure in Allure: `page_url`, `screenshot`, `page_source`, `console_log`; then `quit()` |

Unknown `BROWSER` → fail-fast at session start (`pytest.UsageError`).  
CLI overrides `.env`.

Desktop viewport matters for the category sort dropdown (`d-lg-*` in the stand DOM).  
Default **1920×1080** applies under `--headed` too — on a small physical display a headed sort run may flake; diagnose with headless (same as CI). Tests marked `mobile` use **390×844** instead.

---

## Page fixtures

| Fixture | Class | When |
|---------|-------|------|
| `cart_page` | `CartPage` | empty/filled cart, Checkout CTA, qty/total, remove, reload, modal → cart |
| `category_page` | `CategoryPage` | listing, search (incl. negative), sort, hover ATC, category → PDP |
| `product_page` | `ProductPage` | price, qty, ATC, breadcrumb (`open_with_category`), Terms |

All depend on `driver` (function scope). Typical test:

```python
def test_empty_cart(self, cart_page):
    cart_page.open_page()
    cart_page.verify_cart_is_empty()
```

Using several pages in one test is fine (product → cart, category → PDP):

```python
def test_qty_from_product_reflected_in_cart(self, product_page, cart_page):
    product_page.open_page()
    product_page.set_quantity_via_input("3")
    product_page.add_to_cart()
    cart_page.navigate_to_cart_from_modal()
    cart_page.verify_item_quantity_equals(3)
```

---

## Environment config

Loaded via `python-dotenv` (`load_dotenv` in `conftest` / `BasePage`).

| Variable | Read in |
|----------|---------|
| `BASE_URL` | `BasePage.base_url` |
| `BROWSER` | `driver` fixture (`--browser` overrides) |
| `HEADLESS` | `driver` fixture (`--headed` / `--headless`) |
| `LOCAL_LOG` | pytest `log_file` → `logs/test-run.log` |
| `LOG_LEVEL` | log file level when `LOCAL_LOG` is on |

**Note:** `driver` is **function-scoped** → fresh browser per test (xdist-safe, clean cart on demo stand). See [`architecture.md`](architecture.md) for xdist isolation details.
