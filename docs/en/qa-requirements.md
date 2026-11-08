# QA requirements

Expected UI states, markers, and the scenario map for the Selenium POM suite.

**Language:** English · [Русский](../ru/qa-requirements.md)

Product flows: [`brd.md`](brd.md) · Architecture: [`architecture.md`](architecture.md) · How to run: [`local-run.md`](local-run.md).

---

## Scope

| | |
|--|--|
| Pages under test | category, product (PDP), cart |
| Target size | **~33 test-IDs** (~10–11 per page; `@parametrize` counts as separate IDs) |
| Assert style | `verify_*` on page objects only |
| Out of scope | full checkout/payment, auth, attribute filters, multi-browser matrix in CI |

Selection is **risk-based**: money (cart total), catalog search/sort, input resilience, cross-page data, persistence — not presence-only checks.

---

## Markers

Registered in `pytest.ini`. A test usually has **one page marker** plus one or more severity/type markers.

| Marker | Meaning | Typical use |
|--------|---------|-------------|
| `cart` / `category` / `product` | page area | slice by page (`category`/`product` also include the mobile-viewport variant of that page) |
| `smoke` | minimal confidence suite | PR / quick local check |
| `critical` | high-priority happy path | release gate |
| `medium` | boundaries / secondary flows | fuller regression |
| `negative` | invalid or malicious input | resilience |
| `regression` | cross-page or persistence | session / data passthrough |
| `mobile` | viewport smoke (~390×844) | explicit opt-in; **not** part of `smoke` |

```bash
pytest -m smoke -q
pytest -m mobile -q
pytest -m negative -q
pytest -m regression -q
pytest -m "cart and critical" -q
make smoke   # or: critical | medium | negative | regression | cart | category | product | mobile
```

### Marker combinations → CI jobs

| Marker combo | CI job(s) | Notes |
|--------------|-----------|-------|
| `smoke` | `run-ui-tests` (Chrome) + `smoke-browsers` (Chrome+Firefox) | Default manual run suite |
| `critical` | `run-ui-tests` (Chrome) | Release gate |
| `mobile` | `run-ui-tests` (Chrome, viewport 390×844) | Opt-in, not in `smoke` |
| `negative` | `run-ui-tests` (Chrome) | Resilience checks |
| `regression` | `run-ui-tests` (Chrome) | Cross-page / persistence |
| `cart and critical` | `run-ui-tests` (Chrome) | Page + severity slice |
| (no marker / `all`) | `run-ui-tests` (Chrome, full suite) | Push/PR default |

---

## Test map

Counts below are **collected test-IDs** (parametrized rows expand).

### Category — 11 IDs

| Test | Precondition / data | Expectation | Markers |
|------|---------------------|-------------|---------|
| `test_products_count` | open desks category | product cards count > 0 | category, smoke, critical |
| `test_search_desk` | query `Desk` | every result name contains `desk` | category, smoke, critical |
| `test_hover_add_to_cart` | hover first simple card → ATC (skip configurables) | toast product name matches card | category, critical |
| `test_search_empty_results` | query `NonExistentItem123` | empty-state message + 0 result cards | category, medium |
| `test_search_case_and_partial` | `@parametrize` `DESK`→`desk`, `Des`→`des` | all result names contain expected substring | category, medium |
| `test_search_resilience_malformed_input` | `@parametrize` XSS / SQLi-like strings | no JS alert; search URL; empty results + empty-state (UI resilience, not security audit) | category, negative |
| `test_sort_by_price_ascending` | Sort → Price Low to High | URL contains `order=list_price`; prices ascending | category, medium |
| `test_product_link_navigates_to_detail` | click first product name | PDP `h1` matches card name | category, regression |
| `test_category_products_visible_on_mobile` | open desks at 390×844 | product cards count > 0 (`td.oe_product` still in DOM) | category, mobile |

**Stand notes:** sort navigates to `/shop?order=list_price…&category=…` (leaves category path). Malformed search is treated as **UI resilience** (empty-search outcome), not a penetration test. Sort / hover ATC are **desktop-only** — do not mark them `mobile` (`d-lg-*` / hover). `pytest -m category` includes the mobile viewport variant.

### Product — 11 IDs

| Test | Precondition / data | Expectation | Markers |
|------|---------------------|-------------|---------|
| `test_image_visible` | open PDP | product image present | product, smoke, critical |
| `test_quantity_limits` | default qty = 1; click − | qty stays `1` | product, medium |
| `test_quantity_control` | click + | qty becomes `2` | product, medium |
| `test_add_from_details` | click `#add_to_cart` | confirmation modal present | product, smoke, critical |
| `test_price_is_displayed` | open PDP | visible price parses to > 0 | product, smoke |
| `test_quantity_direct_input_valid` | type `3` into qty | qty equals `3` | product, medium |
| `test_quantity_direct_input_invalid` | `@parametrize` `0`, `abc`; then click + | qty is a positive integer again | product, negative |
| `test_breadcrumb_contains_category` | open PDP with `?category=9` | breadcrumb contains `Multimedia` | product, medium |
| `test_terms_and_conditions_visible` | open PDP | Terms block / link visible | product, smoke |
| `test_product_image_visible_on_mobile` | open PDP at 390×844 | product image present | product, mobile |

**Stand notes:** invalid qty may remain `0`/`abc` until a UI control (`+`) runs — the test asserts **recoverability**, not silent clamp on blur. Breadcrumb shows the category only when opened with `?category=…`. `pytest -m product` includes the mobile viewport variant.

### Cart — 11 IDs

| Test | Precondition / data | Expectation | Markers |
|------|---------------------|-------------|---------|
| `test_empty_cart` | open `/shop/cart` | empty-state message | cart, smoke, critical |
| `test_item_in_cart` | PDP add → View cart | product name listed | cart, critical |
| `test_continue_shopping` | filled cart → Continue shopping | URL path equals `/shop` (not merely contains `/shop`) | cart, medium |
| `test_cart_navigation_via_modal` | PDP add → View cart | URL contains `/shop/cart` | cart, critical |
| `test_cart_update_quantity_recalculates_total` | filled cart; click + on line | qty = 2; total **increases** (no hardcoded amount) | cart, critical |
| `test_cart_quantity_does_not_go_below_one` | filled cart qty=1; click − | line removed (empty cart; stand has no qty&lt;1 row) | cart, medium |
| `test_cart_remove_item_returns_to_empty` | filled cart → Remove | empty-state again | cart, critical |
| `test_checkout_visible_when_items` | filled cart | Checkout CTA present | cart, smoke |
| `test_checkout_absent_when_empty` | empty cart | Checkout CTA absent | cart, negative |
| `test_cart_persists_after_reload` | filled cart → `refresh` | same product still listed | cart, regression |
| `test_qty_from_product_reflected_in_cart` | PDP qty = 3 → cart | cart line qty = 3 | cart, regression |

**Stand notes:** qty/total update via AJAX — waits target value/text change. Checkout (`website_sale_main_button`) exists only when the cart has items.

---

## Taxonomy

| Type | Examples |
|------|----------|
| Positive / happy path | Desk search, hover/PDP ATC, item in cart, Checkout when filled |
| Boundary | PDP qty not below 1; cart − at 1 clears line; empty search; case/partial search |
| Negative | malformed search resilience; invalid qty recovery; Checkout absent when empty |
| Regression | category → PDP; cart after reload; PDP qty → cart qty |

---

## Data-driven cases

| Test | Parameters |
|------|------------|
| `test_search_case_and_partial` | `("DESK", "desk")`, `("Des", "des")` |
| `test_search_resilience_malformed_input` | `<script>alert(1)</script>`, `' OR '1'='1` |
| `test_quantity_direct_input_invalid` | `"0"`, `"abc"` |

Each parameter row is a separate pytest/Allure test-ID.

---

## Allure

| Layer | What we set |
|-------|-------------|
| Feature | page area (`Category` / `Product` / `Cart`) |
| Story | flow group (Search, Checkout CTA, …) |
| Title | human-readable scenario (incl. parametrize placeholders) |
| Steps | `@allure.step` on key page actions |
| Attachments | `page_url` / `screenshot` / `page_source` / `console_log` **on failure only** |
| Environment | `environment.properties` (`Browser`, `Headless`, `LocalLog`, `BaseUrl`, `Python`, `OS`) — auto-generated in `pytest_sessionfinish` |

Triage guide: [`test-analysis.md`](test-analysis.md).

---
 
*Last updated: 2026-11-08*
