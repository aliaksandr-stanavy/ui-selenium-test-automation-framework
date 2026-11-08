# Справочник фикстур

Какие фикстуры есть и когда их использовать.

**Язык:** Русский · [English](../en/fixtures-reference.md)

Архитектура: [`architecture.md`](architecture.md). Карта сценариев: [`qa-requirements.md`](qa-requirements.md).

---

## `driver`

| | |
|--|--|
| Scope | function |
| Назначение | WebDriver (Chrome / Firefox); **1920×1080** по умолчанию, **390×844** для `@pytest.mark.mobile` |
| Env / CLI | `BROWSER` / `--browser`; `HEADLESS` / `--headed`/`--headless`; `LOCAL_LOG` / `--local-log` |
| Default | `chrome`, headless=`true`, local log=`false` |
| Teardown | при падении в Allure: `page_url`, `screenshot`, `page_source`, `console_log`; затем `quit()` |

Неизвестное `BROWSER` → fail-fast на старте (`pytest.UsageError`).  
CLI перекрывает `.env`.

Desktop viewport важен для sort dropdown на category (`d-lg-*` в DOM стенда).  
Default **1920×1080** действует и при `--headed` — на маленьком физическом экране headed-прогон sort может флейкать; для диагностики используйте headless (как в CI). Тесты с маркером `mobile` получают **390×844**.

---

## Page fixtures

| Фикстура | Класс | Когда |
|----------|-------|-------|
| `cart_page` | `CartPage` | empty/filled cart, Checkout CTA, qty/total, remove, reload, modal → cart |
| `category_page` | `CategoryPage` | список, search (в т.ч. negative), sort, hover ATC, category → PDP |
| `product_page` | `ProductPage` | цена, qty, ATC, breadcrumb (`open_with_category`), Terms |

Все зависят от `driver` (function scope). Типичный тест:

```python
def test_empty_cart(self, cart_page):
    cart_page.open_page()
    cart_page.verify_cart_is_empty()
```

Несколько страниц в одном тесте — нормально (product → cart, category → PDP):

```python
def test_qty_from_product_reflected_in_cart(self, product_page, cart_page):
    product_page.open_page()
    product_page.set_quantity_via_input("3")
    product_page.add_to_cart()
    cart_page.navigate_to_cart_from_modal()
    cart_page.verify_item_quantity_equals(3)
```

---

## Конфиг окружения

Загружается через `python-dotenv` (`load_dotenv` в `conftest` / `BasePage`).

| Переменная | Где читается |
|------------|--------------|
| `BASE_URL` | `BasePage.base_url` |
| `BROWSER` | фикстура `driver` (`--browser` перекрывает) |
| `HEADLESS` | фикстура `driver` (`--headed` / `--headless`) |
| `LOCAL_LOG` | pytest `log_file` → `logs/test-run.log` |
| `LOG_LEVEL` | уровень файла лога при `LOCAL_LOG` |

**Примечание:** `driver` — **function-scoped** → свежий браузер на тест (xdist-safe, чистая корзина на демо-стенде). Подробнее в [`architecture.md`](architecture.md).
