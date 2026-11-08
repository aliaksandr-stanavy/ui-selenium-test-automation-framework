# Local run

Pytest commands, markers, Make, and Allure.

**Language:** English · [Русский](../ru/local-run.md)

Quick start: [`quick-start.md`](quick-start.md).

---

## Environment variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BASE_URL` | stand URL | `https://shop.example.com` (override in `.env`) |
| `BROWSER` | `chrome` or `firefox` | `chrome` |
| `HEADLESS` | `true` / `false` — no window / show window | `true` |
| `LOCAL_LOG` | write `logs/test-run.log` | `false` |
| `LOG_LEVEL` | log file level (`INFO`, `DEBUG`, …) | `INFO` |

Priority: **CLI > env > default**.

```bash
# Windows PowerShell
$env:BROWSER="firefox"
$env:HEADLESS="false"
pytest -m smoke
```

---

## Make

| Target | Action |
|--------|--------|
| `make install` | `pip install -r requirements.txt` |
| `make install-dev` | runtime + mypy/pre-commit + git hooks |
| `make lint` / `make mypy` | type checks |
| `make pre-commit` | all pre-commit hooks |
| `make test` / `make all` | full suite |
| `make smoke` | `pytest -m smoke` |
| `make critical` | `pytest -m critical` |
| `make medium` | `pytest -m medium` |
| `make cart` / `category` / `product` | by page marker |
| `make negative` | `pytest -m negative` |
| `make regression` | `pytest -m regression` |
| `make headed` | `pytest --headed` |
| `make firefox` | `pytest --browser firefox` |
| `make log` | `pytest --local-log` |
| `make parallel` | `pytest -n auto` (pytest-xdist; headless only) |
| `make rerun` | `pytest --reruns 1 --reruns-delay 1` (one retry on failure) |
| `make mobile` | `pytest -m mobile` (viewport 390×844) |
| `make run ARGS="…"` | custom pytest flags |
| `make marker M=…` | custom marker |
| `make file F=…` | single test file |
| `make failed` / `make last` | `--lf` / `-x` |
| `make allure` / `make allure-gen` | open / generate-only report |
| `make clean` | remove caches, logs, Allure artifacts (`scripts/local/maintenance/clean.py --yes`) |
| `make clean-dry` | preview what `make clean` would delete |

**`make clean` example output:**
```text
Removed .pytest_cache
Removed .mypy_cache
Removed .ruff_cache
Removed __pycache__ (12 dirs)
Removed allure-results
Removed allure-report
Removed logs
```
 
Without Make: same commands via `pytest` directly.

---

## Pytest

```bash
pytest -q
pytest -m "smoke or critical" -q
pytest tests/test_cart.py -q
pytest --tb=short

# browser / window / log (CLI overrides .env)
pytest -m smoke --headed
pytest -m smoke --browser firefox
pytest -m smoke --headed --browser firefox --local-log
make run ARGS="--headed --browser firefox --local-log"

# parallel (headless only; custom workers via make run)
make parallel
make run ARGS="-n 4 -m smoke"

# mobile viewport (~390×844; not part of smoke)
make mobile
pytest -m mobile --headed
```

`pytest.ini` already sets `--alluredir=allure-results --clean-alluredir`.

**Parallel:** `make parallel` / `pytest -n auto` — headless only. Do not combine with `--headed`; avoid `--local-log` (multiple processes write one file).

**Rerun:** local `make test` has **no** retry (fail immediately). Opt-in: `make rerun` or `make run ARGS="--reruns 1 -m smoke"`. CI always uses `--reruns 1`.

**Mobile:** `make mobile` / `pytest -m mobile` — opt-in viewport smoke (390×844). Not included in `-m smoke`. `pytest -m category` / `-m product` also pick up the matching mobile test (dual markers).

---

## Allure

```bash
pytest
allure serve allure-results
# or:
allure generate allure-results -o allure-report --clean
allure open allure-report
```

After a run: the **Environment** tab (`Browser` / `Headless` / `LocalLog` / `BaseUrl` / `Python` / `OS`) is filled automatically; on fail — `page_url` / `screenshot` / `page_source` / `console_log`.

`allure serve` / `allure generate` need a Java runtime (JRE 8+) on `PATH` — [Allure Commandline](https://allurereport.org/docs/install/) itself is written in Java; the tests do not require Java.

CI: [`ci-cd.md`](ci-cd.md).

---
 
*Last updated: 2026-11-08*
