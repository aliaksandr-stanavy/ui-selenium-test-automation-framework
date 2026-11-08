# BRD — demo shop (UI)

Business / product description of the UI flows covered by this automation suite.

**Language:** English · [Русский](../ru/brd.md)

How we test (markers, expectations, test map): [`qa-requirements.md`](qa-requirements.md).  
Code layout: [`architecture.md`](architecture.md).

---

## Context

| | |
|--|--|
| Product | Demo e-commerce shop (Odoo Website Sale–like) for practicing UI automation |
| Actor | Anonymous shopper (no auth in scope) |
| Goal | Browse a category, open a product, manage cart quantity / remove / checkout CTA |
| Stand URL | `BASE_URL` from env (docs use placeholder `https://shop.example.com`) |
| Automation focus | Category listing, PDP, cart + shared “added to cart” modal |

Representative paths used in the suite:

| Area | Example path |
|------|----------------|
| Category | `/shop/category/desks-1` |
| Product (PDP) | `/shop/furn-9999-office-design-software-7` |
| Product + category crumb | same PDP with `?category=9` → breadcrumb **Multimedia** |
| Cart | `/shop/cart` |

---

## Category

**Entry:** `/shop/category/...` (suite uses desks).

| Capability | Expected behavior |
|------------|-------------------|
| Product grid | Category shows one or more product cards (name, image, price). |
| Search — match | Submitting a search query filters results; result names contain the query (case-insensitive / partial supported). |
| Search — no match | Empty-state message; no result cards. |
| Search — hostile input | XSS / SQLi-like strings do not open a JS `alert` and do not leave a broken blank page. |
| Sort by price | “Price — Low to High” orders visible prices ascending; navigation uses `order=list_price` in the URL (may leave the category path for `/shop?order=…&category=…`). |
| Hover add to cart | Hovering a card reveals Add to cart; click opens the shared confirmation modal with the same product name. |
| Open PDP | Clicking the product name opens the detail page; PDP title matches the card name. |

---

## Product (PDP)

**Entry:** `/shop/<product-slug>` (suite uses Office Design Software).

| Capability | Expected behavior |
|------------|-------------------|
| Media & price | Product image and a positive monetary price are visible. |
| Quantity — controls | Default qty is `1`; decrease does not go below `1`; increase updates the field. |
| Quantity — direct input | Valid numeric input is accepted; after invalid input (`0`, non-numeric), UI controls (e.g. `+`) restore a positive integer. |
| Add to cart | `#add_to_cart` opens the shared confirmation modal. |
| Breadcrumb | With `?category=<id>`, breadcrumb includes the category name (e.g. `Multimedia` for `category=9`). Without it, category crumb may be absent. |
| Legal / shipping blurb | Terms and Conditions block (link to `/terms` and related text) is visible. |

---

## Cart

**Entry:** `/shop/cart`, or via **View cart** from the confirmation modal after add.

| Capability | Expected behavior |
|------------|-------------------|
| Empty state | Empty cart shows an empty-state message; **Checkout** CTA is absent. |
| After add | Product name appears in the cart; **Checkout** CTA is present. |
| Line quantity | Increasing line qty updates the line and **recalculates Total** (AJAX; amount compared before/after, not hardcoded). |
| Remove | Removing the line returns the empty state. |
| Continue shopping | Returns the shopper to the `/shop` area. |
| Persistence | Cart contents survive a full page reload (session). |
| Qty from PDP | Quantity chosen on the PDP is reflected on the cart line after add → View cart. |

---

## Shared “added to cart” modal

Used from **category** (hover ATC) and **product** (PDP ATC). Locators: `MODAL_*` in `pages/locators/cart_locators.py`.

```text
Add to cart (category or PDP)
  → confirmation modal (product name visible)
  → optional: View cart → /shop/cart
```

---

## Non-goals / out of scope
 
Not part of the current automated contract:
 
- Completing checkout (shipping / payment / order confirmation)
- Sign-in / account / wishlist
- Attribute filters (Legs, Duration, price range, pricelist switcher)
- Sort directions other than price ascending (e.g. High to Low) — intentional suite trim
- Multi-item cart edge cases beyond single-line flows covered in tests
- Multi-browser matrix in CI (Firefox remains local via `BROWSER`)
 
## Navigation flow (text diagram)
 
```text
Category (/shop/category/desks-1)
    │
    ├── Search → filtered results
    ├── Sort (Price Low→High) → /shop?order=list_price+asc
    ├── Hover card → Add to cart → Modal → View cart
    └── Click name → PDP (/shop/furn-9999...)
 
PDP
    │
    ├── Image + Price visible
    ├── Qty controls (+/-) / direct input
    ├── Add to cart → Modal → View cart
    ├── Breadcrumb (with ?category= → "Multimedia")
    └── Terms & Conditions block
 
Cart (/shop/cart)
    │
    ├── Empty state (no Checkout)
    ├── Item listed + Checkout visible
    ├── Qty + → Total recalculates (AJAX)
    ├── Remove → Empty state
    ├── Continue shopping → /shop
    ├── Reload → persists (session)
    └── PDP qty → cart qty
```
 
Detailed scenario ↔ expectation map: [`qa-requirements.md`](qa-requirements.md).
