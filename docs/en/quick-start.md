# Quick start

Run the UI tests in ~5 minutes.

**Language:** English · [Русский](../ru/quick-start.md)

## 1. Clone and venv

```bash
git clone https://github.com/aliaksandr-stanavy/ui-selenium-test-automation-framework.git
cd ui-selenium-test-automation-framework

python -m venv .venv
# Windows:
.venv\Scripts\activate
# Unix:
source .venv/bin/activate

pip install -r requirements.txt
# optional (mypy + pre-commit): make install-dev
```

Requires Python 3.12+ and Chrome (or Firefox). Selenium Manager resolves the driver.

## 2. `.env` config

```bash
copy .env.example .env   # Windows
# cp .env.example .env   # Unix
```

| Variable | Example | Required |
|----------|---------|----------|
| `BASE_URL` | `<your-stand-url>` | yes |
| `BROWSER` | `chrome` | no (default `chrome`) |
| `HEADLESS` | `true` | no (default `true`) |
| `LOCAL_LOG` | `false` | no |

Use your stand URL. Public examples use the placeholder `https://shop.example.com`.

Show the browser window: `pytest -m smoke --headed` (or `HEADLESS=false`).

## 3. Run

```bash
make smoke
# or:
pytest -m smoke -q
```

Full suite (~33 tests): `make all` / `pytest`.

Other slices: `make critical`, `make negative`, `make regression`, `make mobile` — see [local-run](local-run.md).

Scenario map: [qa-requirements](qa-requirements.md).

## 4. Allure (local)

```bash
pytest
allure serve allure-results
```

Requires [Allure Commandline](https://allurereport.org/docs/install/) and a Java runtime (JRE 8+) on `PATH` — the CLI itself is written in Java.

Next: [architecture](architecture.md) · [local-run](local-run.md) · [troubleshooting](troubleshooting.md).

---
 
*Last updated: 2026-11-08*
