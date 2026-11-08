# QA-требования

Ожидаемые UI-состояния, маркеры и карта сценариев Selenium POM suite.

**Язык:** Русский · [English](../en/qa-requirements.md)

UI-flows: [`brd.md`](brd.md) · Архитектура: [`architecture.md`](architecture.md) · Запуск: [`local-run.md`](local-run.md).

---

## Скоуп

| | |
|--|--|
| Страницы | category, product (PDP), cart |
| Целевой размер | **~33 test-ID** (~10–11 на страницу; `@parametrize` даёт отдельные ID) |
| Asserts | только `verify_*` на page objects |
| Вне скоупа | полный checkout/оплата, авторизация, фильтры атрибутов, multi-browser matrix в CI |

Отбор **risk-based**: деньги (total корзины), поиск/сортировка каталога, устойчивость к вводу, сквозные данные, persistence — не presence-only проверки.

---

## Маркеры

Зарегистрированы в `pytest.ini`. Обычно у теста **один page-маркер** плюс один или несколько severity/type.

| Маркер | Смысл | Типичное использование |
|--------|-------|------------------------|
| `cart` / `category` / `product` | область страницы | срез по странице (`category`/`product` также включают mobile-viewport вариант той же страницы) |
| `smoke` | минимальный confidence suite | PR / быстрый локальный прогон |
| `critical` | высокий приоритет happy-path | релизный gate |
| `medium` | границы / вторичные сценарии | более полный regression |
| `negative` | невалидный или вредоносный ввод | resilience |
| `regression` | сквозной или persistence | session / передача данных |
| `mobile` | viewport smoke (~390×844) | явный opt-in; **не** входит в `smoke` |

```bash
pytest -m smoke -q
pytest -m mobile -q
pytest -m negative -q
pytest -m regression -q
pytest -m "cart and critical" -q
make smoke   # или: critical | medium | negative | regression | cart | category | product | mobile
```

### Комбинации маркеров → CI jobs

| Маркеры | CI job(s) | Примечание |
|---------|-----------|------------|
| `smoke` | `run-ui-tests` (Chrome) + `smoke-browsers` (Chrome+Firefox) | Default ручной запуск |
| `critical` | `run-ui-tests` (Chrome) | Релизный gate |
| `mobile` | `run-ui-tests` (Chrome, viewport 390×844) | Opt-in, не в `smoke` |
| `negative` | `run-ui-tests` (Chrome) | Проверки resilience |
| `regression` | `run-ui-tests` (Chrome) | Сценарии cross-page / persistence |
| `cart and critical` | `run-ui-tests` (Chrome) | Срез page + severity |
| (без маркера / `all`) | `run-ui-tests` (Chrome, полный suite) | Push/PR по умолчанию |

---

## Карта тестов

Ниже — **собранные test-ID** (строки parametrize считаются отдельно).

### Category — 11 ID

| Тест | Предусловие / данные | Ожидание | Маркеры |
|------|----------------------|----------|---------|
| `test_products_count` | открыть категорию desks | число карточек > 0 | category, smoke, critical |
| `test_search_desk` | запрос `Desk` | каждое имя результата содержит `desk` | category, smoke, critical |
| `test_hover_add_to_cart` | hover первой простой карточки → ATC (skip configurable) | имя в toast = имя карточки | category, critical |
| `test_search_empty_results` | запрос `NonExistentItem123` | empty-state + 0 карточек результатов | category, medium |
| `test_search_case_and_partial` | `@parametrize` `DESK`→`desk`, `Des`→`des` | все имена содержат ожидаемую подстроку | category, medium |
| `test_search_resilience_malformed_input` | `@parametrize` XSS / SQLi-like | нет JS alert; search URL; empty results + empty-state (UI resilience, не security audit) | category, negative |
| `test_sort_by_price_ascending` | Sort → Price Low to High | URL содержит `order=list_price`; цены по возрастанию | category, medium |
| `test_product_link_navigates_to_detail` | клик по имени первого товара | `h1` на PDP = имя карточки | category, regression |
| `test_category_products_visible_on_mobile` | desks на 390×844 | число карточек > 0 (`td.oe_product` остаётся в DOM) | category, mobile |

**Заметки по стенду:** sort уводит на `/shop?order=list_price…&category=…` (path category меняется). Malformed search — **UI resilience** (empty-search), не penetration test. Sort / hover ATC — **только desktop**, не помечать `mobile` (`d-lg-*` / hover). `pytest -m category` включает mobile-viewport вариант.

### Product — 11 ID

| Тест | Предусловие / данные | Ожидание | Маркеры |
|------|----------------------|----------|---------|
| `test_image_visible` | открыть PDP | изображение товара есть | product, smoke, critical |
| `test_quantity_limits` | qty по умолчанию 1; клик − | qty остаётся `1` | product, medium |
| `test_quantity_control` | клик + | qty становится `2` | product, medium |
| `test_add_from_details` | клик `#add_to_cart` | модалка подтверждения | product, smoke, critical |
| `test_price_is_displayed` | открыть PDP | цена парсится в значение > 0 | product, smoke |
| `test_quantity_direct_input_valid` | ввод `3` в qty | qty = `3` | product, medium |
| `test_quantity_direct_input_invalid` | `@parametrize` `0`, `abc`; затем клик + | qty снова положительное целое | product, negative |
| `test_breadcrumb_contains_category` | PDP с `?category=9` | breadcrumb содержит `Multimedia` | product, medium |
| `test_terms_and_conditions_visible` | открыть PDP | блок / ссылка Terms видна | product, smoke |
| `test_product_image_visible_on_mobile` | PDP на 390×844 | изображение товара есть | product, mobile |

**Заметки по стенду:** невалидный qty может остаться `0`/`abc` до клика `+` — тест проверяет **восстанавливаемость**, а не silent clamp на blur. Категория в breadcrumb появляется только при `?category=…`. `pytest -m product` включает mobile-viewport вариант.

### Cart — 11 ID

| Тест | Предусловие / данные | Ожидание | Маркеры |
|------|----------------------|----------|---------|
| `test_empty_cart` | открыть `/shop/cart` | empty-state сообщение | cart, smoke, critical |
| `test_item_in_cart` | PDP add → View cart | имя товара в списке | cart, critical |
| `test_continue_shopping` | заполненная корзина → Continue shopping | path URL равен `/shop` (не просто содержит `/shop`) | cart, medium |
| `test_cart_navigation_via_modal` | PDP add → View cart | URL содержит `/shop/cart` | cart, critical |
| `test_cart_update_quantity_recalculates_total` | корзина; клик + на строке | qty = 2; total **растёт** (без хардкода суммы) | cart, critical |
| `test_cart_quantity_does_not_go_below_one` | корзина qty=1; клик − | строка удаляется (пустая корзина; на стенде нет qty&lt;1) | cart, medium |
| `test_cart_remove_item_returns_to_empty` | корзина → Remove | снова empty-state | cart, critical |
| `test_checkout_visible_when_items` | заполненная корзина | Checkout CTA есть | cart, smoke |
| `test_checkout_absent_when_empty` | пустая корзина | Checkout CTA нет | cart, negative |
| `test_cart_persists_after_reload` | корзина → `refresh` | тот же товар на месте | cart, regression |
| `test_qty_from_product_reflected_in_cart` | PDP qty = 3 → cart | qty в строке корзины = 3 | cart, regression |

**Заметки по стенду:** qty/total обновляются AJAX — waits на смену value/текста. Checkout (`website_sale_main_button`) есть только при непустой корзине.

---

## Таксономия

| Тип | Примеры |
|-----|---------|
| Позитив / happy path | поиск Desk, hover/PDP ATC, товар в корзине, Checkout при товарах |
| Граница | PDP qty не ниже 1; в корзине − при 1 удаляет строку; пустой поиск; case/partial search |
| Негатив | resilience malformed search; восстановление после invalid qty; нет Checkout на пустой |
| Regression | category → PDP; корзина после reload; PDP qty → cart qty |

---

## Data-driven кейсы

| Тест | Параметры |
|------|-----------|
| `test_search_case_and_partial` | `("DESK", "desk")`, `("Des", "des")` |
| `test_search_resilience_malformed_input` | `<script>alert(1)</script>`, `' OR '1'='1` |
| `test_quantity_direct_input_invalid` | `"0"`, `"abc"` |

Каждая строка параметров — отдельный pytest/Allure test-ID.

---

## Allure

| Слой | Что задаём |
|------|------------|
| Feature | область страницы (`Category` / `Product` / `Cart`) |
| Story | группа сценария (Search, Checkout CTA, …) |
| Title | человекочитаемый сценарий (в т.ч. placeholders parametrize) |
| Steps | `@allure.step` на ключевых page-действиях |
| Attachments | `page_url` / `screenshot` / `page_source` / `console_log` **только при fail** |
| Environment | `environment.properties` (`Browser`, `Headless`, `LocalLog`, `BaseUrl`, `Python`, `OS`) — автогенерация в `pytest_sessionfinish` |

Разбор падений: [`test-analysis.md`](test-analysis.md).

---
 
*Last updated: 2026-11-08*
