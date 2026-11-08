# BRD — демо-магазин (UI)

Продуктовое описание UI-flows, которые покрывает этот suite автотестов.

**Язык:** Русский · [English](../en/brd.md)

Как тестируем (маркеры, ожидания, карта тестов): [`qa-requirements.md`](qa-requirements.md).  
Устройство кода: [`architecture.md`](architecture.md).

---

## Контекст

| | |
|--|--|
| Продукт | Демо интернет-магазин (Odoo Website Sale–like) для практики UI-автоматизации |
| Актор | Анонимный покупатель (auth вне скоупа) |
| Цель | Каталог категории → карточка товара → корзина (qty / remove / Checkout CTA) |
| URL стенда | `BASE_URL` из env (в docs — placeholder `https://shop.example.com`) |
| Фокус автоматизации | Category listing, PDP, cart + общая модалка «added to cart» |

Пути, которые использует suite:

| Область | Пример path |
|---------|-------------|
| Category | `/shop/category/desks-1` |
| Product (PDP) | `/shop/furn-9999-office-design-software-7` |
| Product + category в breadcrumb | тот же PDP с `?category=9` → **Multimedia** |
| Cart | `/shop/cart` |

---

## Category

**Вход:** `/shop/category/...` (в suite — desks).

| Возможность | Ожидаемое поведение |
|-------------|---------------------|
| Сетка товаров | На категории есть одна или несколько карточек (имя, изображение, цена). |
| Поиск — совпадение | Запрос фильтрует результаты; имена содержат запрос (case-insensitive / partial). |
| Поиск — без совпадений | Empty-state сообщение; нет карточек результатов. |
| Поиск — враждебный ввод | XSS / SQLi-like строки не открывают JS `alert` и не оставляют «битую» пустую страницу. |
| Сортировка по цене | «Price — Low to High» упорядочивает цены по возрастанию; в URL появляется `order=list_price` (path может смениться на `/shop?order=…&category=…`). |
| Hover add to cart | Hover по карточке → Add to cart → общая модалка с тем же именем товара. |
| Открытие PDP | Клик по имени товара открывает детальную страницу; заголовок PDP совпадает с карточкой. |

---

## Product (PDP)

**Вход:** `/shop/<product-slug>` (в suite — Office Design Software).

| Возможность | Ожидаемое поведение |
|-------------|---------------------|
| Медиа и цена | Видны изображение и положительная денежная цена. |
| Qty — кнопки | По умолчанию `1`; уменьшить ниже `1` нельзя; `+` обновляет поле. |
| Qty — прямой ввод | Валидное число принимается; после невалидного (`0`, нечисло) UI-контролы (например `+`) возвращают положительное целое. |
| Add to cart | `#add_to_cart` открывает общую модалку подтверждения. |
| Breadcrumb | С `?category=<id>` в хлебных крошках есть имя категории (для `category=9` — `Multimedia`). Без query категория может отсутствовать. |
| Terms | Блок Terms and Conditions (ссылка `/terms` и сопутствующий текст) виден на PDP. |

---

## Cart

**Вход:** `/shop/cart` или **View cart** из модалки после добавления.

| Возможность | Ожидаемое поведение |
|-------------|---------------------|
| Пустая корзина | Empty-state сообщение; кнопки **Checkout** нет. |
| После add | Имя товара в списке; **Checkout** видна. |
| Qty строки | Увеличение qty обновляет строку и **пересчитывает Total** (AJAX; сравнение до/после, без хардкода суммы). |
| Удаление | Remove возвращает empty-state. |
| Continue shopping | Возврат в область `/shop`. |
| Persistence | Содержимое корзины переживает reload страницы (session). |
| Qty с PDP | Количество, выбранное на PDP, отражается в строке корзины после add → View cart. |

---

## Общая модалка «added to cart»

Используется из **category** (hover ATC) и **product** (PDP ATC). Локаторы: `MODAL_*` в `pages/locators/cart_locators.py`.

```text
Add to cart (category или PDP)
  → модалка подтверждения (видно имя товара)
  → опционально: View cart → /shop/cart
```

---

## Вне скоупа / non-goals

Не входят в текущий автоматизированный контракт:

- Завершение checkout (shipping / payment / подтверждение заказа)
- Sign-in / аккаунт / wishlist
- Фильтры атрибутов (Legs, Duration, price range, pricelist)
- Прочие направления sort (например High to Low) — сознательно урезаны в suite
- Multi-item edge cases сверх однострочных сценариев в тестах
- Multi-browser matrix в CI (Firefox — локально через `BROWSER`)

Детальная карта сценарий ↔ ожидание: [`qa-requirements.md`](qa-requirements.md).
