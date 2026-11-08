# Анализ результатов тестов

Как разбирать падения UI-автотестов (~33 сценариев).

**Язык:** Русский · [English](../en/test-analysis.md)

Карта ожиданий: [`qa-requirements.md`](qa-requirements.md).

---

## Источники сигнала

1. **Трассировка pytest** (`--tb=short`) — assert message, файл, строка.
2. **Allure** — шаги до точки падения; вложения только при fail:
   - `page_url` (TEXT) — URL на момент падения;
   - `screenshot` (PNG);
   - `page_source` (HTML, truncated) — DOM;
   - `console_log` (TEXT) — Chrome browser logs; Firefox — N/A текст.
   Вкладка **Environment** — `browser` / `headless` / `BaseUrl` / OS (из `environment.properties`).
3. **CI artifact** `allure-results-raw` / отчёт на Pages (smoke matrix: отдельно `allure-smoke-*`).

---

## Типичные причины

| Симптом | Куда смотреть |
|---------|----------------|
| `TimeoutException` / wait | локатор, slow UI, flaky search/modal |
| Assert текста / empty state | локализация стенда, другой empty message |
| URL не содержит ожидаемое | редирект, `BASE_URL`, modal не открылась |
| Sort: цены не по возрастанию / timeout URL | клик уводит на `/shop?order=list_price…`; wait по URL, не по path category |
| Cart total / qty не обновились | AJAX: wait на смену `input.js_quantity` / `#order_total` |
| Invalid qty assert | после прямого ввода UI может оставить `0`/`abc` до клика `+` (см. `recover_quantity_via_increase`) |
| Malicious search: «нет search form» | результат может быть на `/website/search` без category form — проверяем «страница жива», не форму |
| Element not clickable | overlay, cookie banner, нужен scroll; sort — desktop viewport |
| Screenshot «не тот» экран | шаг до assert; сравнить с `page_url` / `page_source` |
| JS-ошибка / пустой UI | `console_log` в Allure (Chrome) |

---

## Порядок разбора

1. Открыть failed test в Allure → последний step.
2. Посмотреть `screenshot` + `page_url` + при необходимости `page_source` / `console_log`.
3. Сопоставить с локатором в `pages/locators/` и методом page object.
4. При flaky wait — усилить условие (visibility / URL / text / value change), **не** `time.sleep`.
5. Перепрогнать локально: `pytest path::Test::test_name --tb=short`.

Troubleshooting env/driver: [`troubleshooting.md`](troubleshooting.md).
