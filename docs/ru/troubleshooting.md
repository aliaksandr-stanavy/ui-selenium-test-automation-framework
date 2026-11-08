# Troubleshooting

Типичные проблемы окружения и запуска.

**Язык:** Русский · [English](../en/troubleshooting.md)

---

## `BASE_URL` / стенд
 
- Пустой или placeholder URL → страницы не открываются / 404.
- Решение: скопировать `.env.example` → `.env`, указать реальный стенд.
- В CI задать Secret `BASE_URL`.
 
---
 
## Стенд недоступен / 5xx
 
- Демо-стенд возвращает 5xx / таймауты / недоступен
- Симптомы: `TimeoutException` при загрузке страницы, `ConnectionError`, все тесты падают
- Решение: проверить URL стенда в браузере; если стенд лежит — подождать или использовать другой стенд; CI упадёт честно (без маскировки)
 
---
 
## Драйвер / браузер

| Проблема | Что сделать |
|----------|-------------|
| Chrome не стартует | обновить Chrome; Selenium Manager сам скачает driver |
| Firefox | `BROWSER=firefox` или `--browser firefox`; размер окна в коде (1920×1080 default / 390×844 для `mobile`) |
| Headless отличие от UI | default — headless как в CI; headed: `HEADLESS=false` или `--headed` |
| Sort dropdown «не виден» | нужен desktop width (фикстура уже 1920×1080 для non-mobile тестов) |
| Headed + маленький экран | окно может не получить 1920×1080 → flaky sort; диагностируйте headless-прогоном |
| Маркер `mobile` | переключает viewport на 390×844; sort и hover ATC туда не входят намеренно — не помечайте их `mobile` |
| Локальный лог | `--local-log` или `LOCAL_LOG=true` → `logs/test-run.log` |
| Шум Chrome в консоли (DevTools / AMD / GCM, кракозябры) | подавляется в `_build_chrome_options` (`--log-level=3`, `excludeSwitches`); framework-логи — только через `--local-log` |
| Падения только под `-n` / `make parallel` | скорее нагрузка на демо-стенд (rate limit/таймауты), не гонка по данным — сессии изолированы; воспроизведите последовательно (`make smoke`) |
| `--local-log` + parallel | не рекомендуется: несколько процессов пишут в один `logs/test-run.log` |

Неизвестный `BROWSER` → ошибка на старте сессии (fail-fast), не на первом тесте.

---

## Timeout / flaky

- Не добавлять `time.sleep`.
- Проверить локатор и wait (visibility / URL contains / text / attribute value).
- Поиск: JS-fill — осознанный workaround; при смене UI пересмотреть.
- Корзина: qty/total обновляются AJAX — ждать смену значения, не фиксированный sleep.
- Sort: после клика URL меняется на `/shop?order=…` — ждать `order=list_price` в URL.
- Красный локально без rerun, зелёный в CI с `--reruns 1` → вероятный flake: стабилизировать wait / завести issue, **не** поднимать число reruns.
- Не комбинировать `--reruns` с `--pdb` (плагин несовместим).

---

## Cookie / modal

- Overlay может перекрывать клик — смотреть screenshot.
- Метод `navigate_to_cart_from_modal` ждёт modal и кликает View cart.
- ATC на PDP — `#add_to_cart`.

---

## Allure пустой / старый

- `pytest.ini` чистит `allure-results` на каждый прогон (`--clean-alluredir`).
- Смотреть свежий `allure serve` после текущего прогона.
- При падении в CI смотреть аттачи `page_url` / `screenshot` / `page_source` / `console_log` (Firefox: console — N/A текст).

---

## Allure CLI

| Проблема | Что сделать |
|----------|-------------|
| `'allure' is not recognized` / `command not found` | Установить [Allure Commandline](https://allurereport.org/docs/install/) и добавить в `PATH`; в CI ставится через `npm install -g allure-commandline` |
| `Error: could not find java` / CLI не стартует | Установить JRE 8+ (в CI — Temurin 17) и проверить `java -version` в `PATH` |
| `allure serve` открывает старый отчёт | `pytest.ini` чистит `allure-results` на каждый прогон; смотреть свежий `allure serve` после текущего прогона (см. раздел выше «Allure пустой / старый») |

---

## Зависимости

```bash
pip install -r requirements.txt
python -c "import selenium, pytest, allure, dotenv; print('ok')"
```

Анализ падений: [`test-analysis.md`](test-analysis.md).

---
 
*Last updated: 2026-11-08*
