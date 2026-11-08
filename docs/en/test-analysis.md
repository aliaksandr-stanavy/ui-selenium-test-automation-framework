# Test analysis

How to triage UI automation failures (~33 scenarios).

**Language:** English · [Русский](../ru/test-analysis.md)

Expectation map: [`qa-requirements.md`](qa-requirements.md).

---

## Signal sources

1. **Pytest traceback** (`--tb=short`) — assert message, file, line.
2. **Allure** — steps up to the failure; attachments on failure only:
   - `page_url` (TEXT) — URL at failure time;
   - `screenshot` (PNG);
   - `page_source` (HTML, truncated) — DOM;
   - `console_log` (TEXT) — Chrome browser logs; Firefox — N/A note.
   **Environment** tab — `browser` / `headless` / `BaseUrl` / OS (from `environment.properties`).
3. **CI artifact** `allure-results-raw` / Pages report (smoke matrix: separate `allure-smoke-*`).

---

## Common causes

| Symptom | Check |
|---------|-------|
| `TimeoutException` / wait | locator, slow UI, flaky search/modal |
| Text / empty-state assert | stand locale, different empty message |
| URL missing expected part | redirect, `BASE_URL`, modal did not open |
| Sort: prices not ascending / URL timeout | click navigates to `/shop?order=list_price…`; wait on URL, not category path |
| Cart total / qty did not update | AJAX: wait for `input.js_quantity` / `#order_total` change |
| Invalid qty assert | after direct input UI may keep `0`/`abc` until `+` (`recover_quantity_via_increase`) |
| Malicious search: “no search form” | results may land on `/website/search` without category form — assert page alive, not the form |
| Element not clickable | overlay, cookie banner, needs scroll; sort needs desktop viewport |
| “Wrong” screenshot | step before assert; compare with `page_url` / `page_source` |
| JS error / blank UI | `console_log` in Allure (Chrome) |

---

## Triage order

1. Open the failed test in Allure → last step.
2. Inspect `screenshot` + `page_url`, then `page_source` / `console_log` if needed.
3. Map to locator in `pages/locators/` and the page method.
4. For flaky waits — strengthen the condition (visibility / URL / text / value change), **not** `time.sleep`.
5. Re-run locally: `pytest path::Test::test_name --tb=short`.

Env/driver issues: [`troubleshooting.md`](troubleshooting.md).
