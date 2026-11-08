# Troubleshooting

Common environment and run issues.

**Language:** English · [Русский](../ru/troubleshooting.md)

---

## `BASE_URL` / stand
 
- Empty or placeholder URL → pages fail to load / 404.
- Fix: copy `.env.example` → `.env`, set a real stand URL.
- In CI set Secret `BASE_URL`.
 
---
 
## Stand down / 5xx
 
- Demo stand returns 5xx / times out / unreachable
- Symptoms: `TimeoutException` on page load, `ConnectionError`, all tests fail
- Fix: verify stand URL in browser; if down, wait or use a different stand; CI will fail honestly (no masking)
 
---
 
## Driver / browser

| Issue | What to do |
|-------|------------|
| Chrome won’t start | update Chrome; Selenium Manager downloads the driver |
| Firefox | `BROWSER=firefox` or `--browser firefox`; window size set in code (1920×1080 default / 390×844 for `mobile`) |
| Headless differs from UI | default is headless like CI; headed: `HEADLESS=false` or `--headed` |
| Sort dropdown “not visible” | needs desktop width (fixture already uses 1920×1080 for non-mobile tests) |
| Headed + small screen | window may not reach 1920×1080 → flaky sort; diagnose with a headless run |
| `mobile` marker | switches viewport to 390×844; sort and hover ATC are intentionally excluded — do not mark them `mobile` |
| Local log | `--local-log` or `LOCAL_LOG=true` → `logs/test-run.log` |
| Chrome console noise (DevTools / AMD / GCM, mojibake) | suppressed in `_build_chrome_options` (`--log-level=3`, `excludeSwitches`); framework logs use `--local-log` only |
| Failures only under `-n` / `make parallel` | usually demo-stand load (rate limit/timeouts), not a data race — sessions are isolated; reproduce sequentially (`make smoke`) |
| `--local-log` + parallel | not recommended: multiple processes write one `logs/test-run.log` |

Unknown `BROWSER` → session-start error (fail-fast), not on the first test.

---

## Timeout / flaky

- Do not add `time.sleep`.
- Check locator and wait (visibility / URL contains / text / attribute value).
- Search: JS-fill is an intentional workaround; revisit if the UI changes.
- Cart: qty/total update via AJAX — wait for value change, not a fixed sleep.
- Sort: after click, URL becomes `/shop?order=…` — wait for `order=list_price` in the URL.
- Red locally without rerun, green in CI with `--reruns 1` → likely flake: stabilize the wait / open an issue; do **not** raise reruns.
- Do not combine `--reruns` with `--pdb` (plugin incompatibility).

---

## Cookie / modal

- An overlay may block clicks — check the screenshot.
- `navigate_to_cart_from_modal` waits for the modal and clicks View cart.
- PDP ATC uses `#add_to_cart`.

---

## Empty / stale Allure

- `pytest.ini` cleans `allure-results` every run (`--clean-alluredir`).
- Serve a fresh report after the current run.
- On CI failures check attachments `page_url` / `screenshot` / `page_source` / `console_log` (Firefox: console is an N/A text note).

---

## Allure CLI

| Issue | What to do |
|-------|------------|
| `'allure' is not recognized` / `command not found` | Install [Allure Commandline](https://allurereport.org/docs/install/) and add it to `PATH`; CI installs it via `npm install -g allure-commandline` |
| `Error: could not find java` / CLI won't start | Install a JRE 8+ (CI uses Temurin 17) and confirm `java -version` works on `PATH` |
| `allure serve` shows a stale report | `pytest.ini` cleans `allure-results` every run; serve a fresh report after the current run (see the "Empty / stale Allure" section above) |

---

## Dependencies

```bash
pip install -r requirements.txt
python -c "import selenium, pytest, allure, dotenv; print('ok')"
```

Failure triage: [`test-analysis.md`](test-analysis.md).

---
 
*Last updated: 2026-11-08*
