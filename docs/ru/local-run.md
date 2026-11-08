# Локальный запуск

Команды pytest, маркеры, Make и Allure.

**Язык:** Русский · [English](../en/local-run.md)

Быстрый старт: [`quick-start.md`](quick-start.md).

---

## Переменные окружения

| Переменная | Описание | Default |
|------------|----------|---------|
| `BASE_URL` | URL стенда | `https://shop.example.com` (замените в `.env`) |
| `BROWSER` | `chrome` или `firefox` | `chrome` |
| `HEADLESS` | `true` / `false` — без окна / с окном | `true` |
| `LOCAL_LOG` | писать `logs/test-run.log` | `false` |
| `LOG_LEVEL` | уровень файла лога (`INFO`, `DEBUG`, …) | `INFO` |

Приоритет: **CLI > env > default**.

```bash
# Windows PowerShell
$env:BROWSER="firefox"
$env:HEADLESS="false"
pytest -m smoke
```

---

## Make

| Target | Действие |
|--------|----------|
| `make install` | `pip install -r requirements.txt` |
| `make install-dev` | runtime + mypy/pre-commit + git hooks |
| `make lint` / `make mypy` | проверка типов |
| `make pre-commit` | все pre-commit hooks |
| `make test` / `make all` | весь suite |
| `make smoke` | `pytest -m smoke` |
| `make critical` | `pytest -m critical` |
| `make medium` | `pytest -m medium` |
| `make cart` / `category` / `product` | по page-маркеру |
| `make negative` | `pytest -m negative` |
| `make regression` | `pytest -m regression` |
| `make headed` | `pytest --headed` |
| `make firefox` | `pytest --browser firefox` |
| `make log` | `pytest --local-log` |
| `make parallel` | `pytest -n auto` (pytest-xdist; только headless) |
| `make rerun` | `pytest --reruns 1 --reruns-delay 1` (один повтор при падении) |
| `make mobile` | `pytest -m mobile` (viewport 390×844) |
| `make run ARGS="…"` | произвольные флаги pytest |
| `make marker M=…` | произвольный маркер |
| `make file F=…` | один файл тестов |
| `make failed` / `make last` | `--lf` / `-x` |
| `make allure` / `make allure-gen` | открыть / только сгенерировать отчёт |
| `make clean` | удалить кэши, логи, Allure-артефакты (`scripts/local/maintenance/clean.py --yes`) |
| `make clean-dry` | показать, что удалит `make clean` |

**Пример вывода `make clean`:**
```text
Removed .pytest_cache
Removed .mypy_cache
Removed .ruff_cache
Removed __pycache__ (12 dirs)
Removed allure-results
Removed allure-report
Removed logs
```
 
Без Make: те же команды через `pytest` напрямую.

---

## Pytest

```bash
pytest -q
pytest -m "smoke or critical" -q
pytest tests/test_cart.py -q
pytest --tb=short

# браузер / окно / лог (CLI перекрывает .env)
pytest -m smoke --headed
pytest -m smoke --browser firefox
pytest -m smoke --headed --browser firefox --local-log
make run ARGS="--headed --browser firefox --local-log"

# parallel (headless only; custom workers via make run)
make parallel
make run ARGS="-n 4 -m smoke"

# mobile viewport (~390×844; не входит в smoke)
make mobile
pytest -m mobile --headed
```

`pytest.ini` уже задаёт `--alluredir=allure-results --clean-alluredir`.

**Parallel:** `make parallel` / `pytest -n auto` — только headless. Не комбинировать с `--headed` и не рекомендуется с `--local-log` (несколько процессов пишут в один файл).

**Rerun:** локально `make test` **без** retry (fail сразу). Opt-in: `make rerun` или `make run ARGS="--reruns 1 -m smoke"`. В CI всегда `--reruns 1`.

**Mobile:** `make mobile` / `pytest -m mobile` — opt-in viewport smoke (390×844). Не входит в `-m smoke`. `pytest -m category` / `-m product` также подхватывают соответствующий mobile-тест (двойные маркеры).

---

## Allure

```bash
pytest
allure serve allure-results
# или:
allure generate allure-results -o allure-report --clean
allure open allure-report
```

После прогона: вкладка **Environment** (`Browser` / `Headless` / `LocalLog` / `BaseUrl` / `Python` / `OS`) заполняется автоматически; при fail — `page_url` / `screenshot` / `page_source` / `console_log`.

`allure serve` / `allure generate` требуют установленный Java runtime (JRE 8+) в `PATH` — [Allure Commandline](https://allurereport.org/docs/install/) написан на Java, сами тесты Java не требуют.

CI: [`ci-cd.md`](ci-cd.md).

---
 
*Last updated: 2026-11-08*
