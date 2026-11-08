# 🧪 Shop UI — Test Automation (Selenium)

**Language:** [Русский](README.md) · English

[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Pytest-7.4.3-0A9EDC?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.15.2-43B02A?logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![Allure](https://img.shields.io/badge/Allure-2.13.2-purple?logo=allure&logoColor=white)](https://allurereport.org/)
[![CI](https://github.com/aliaksandr-stanavy/ui-selenium-test-automation-framework/actions/workflows/ui-tests.yml/badge.svg)](https://github.com/aliaksandr-stanavy/ui-selenium-test-automation-framework/actions/workflows/ui-tests.yml)
[![Allure Report](https://img.shields.io/badge/Allure-GitHub%20Pages-orange?logo=allure&logoColor=white)](https://aliaksandr-stanavy.github.io/ui-selenium-test-automation-framework/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-aliaksandr--stanavy-181717?logo=github&logoColor=white)](https://github.com/aliaksandr-stanavy)

**UI test automation framework** for a demo shop built with Python + Pytest + Selenium + Allure (Page Object Model).

> This project is a **demonstration of an industrial approach** to UI testing: lean POM, stable waits, risk-based scenarios, Allure, and a full CI/CD pipeline.
>
> **Portfolio project** — demonstrating production-grade UI automation: lean POM, explicit waits, Allure + Pages, cross-browser CI.

| Start | Documentation |
|-------|-----------------|
| [Quick start](docs/en/quick-start.md) (~5 min) | [EN index](docs/en/index.md) · [RU](docs/ru/index.md) · [languages](docs/README.md) |

---

## 📖 About

The framework shows how to build UI automation infrastructure focused on **reliability, maintainability, and transparent results**.

**Key features:**
- 🏗️ **Page Object Model** — `BasePage` → pages, locators isolated under `pages/locators/`.
- 📊 **Allure reports** — steps; on failure: screenshot, URL, page_source, console; Environment tab (browser, BASE_URL, OS).
- 🏷️ **Markers** — page (`cart` / `category` / `product`) + priority (`smoke` / `critical` / `medium` / `negative` / `regression`) + `mobile` viewport.
- ⏱️ **Explicit waits** — no `time.sleep`, no `implicitly_wait`; custom expected condition.
- 🌐 **Browser via env/CLI** — `BROWSER=chrome|firefox`, `HEADLESS`, optional `--headed` / `--local-log`.
- 📱 **Mobile viewport smoke** — `make mobile` / `-m mobile` at 390×844 (desktop sort/`d-lg-*` excluded).
- 🧩 **CI cross-browser smoke** — Chrome + Firefox matrix on `-m smoke`; full regression / Pages — Chrome only.
- ⚡ **Parallel runs** — `pytest-xdist` (`make parallel` / CI `-n 2`); function-scoped driver = session isolation.
- 🔁 **Flaky reruns** — CI `--reruns 1`; locally opt-in (`make rerun`), default without retry.
- ⚙️ **CI/CD** — GitHub Actions with automatic report publishing to GitHub Pages.
- 🛡️ **Static analysis** — mypy + pre-commit hooks in CI.

### 🔥 What this demonstrates

- **Lean POM:** assertions only in `verify_*` on page objects — no overengineering.
- **Stable synchronization:** explicit waits + `text_to_be_not_empty`, boundary waits without false positives.
- **Risk-based UI flows:** search/sort, hover ATC, quantity boundaries, cart, persistence, resilience to malformed input.
- **Code quality:** typed page layer (mypy), pre-commit in CI.
- **Full reporting loop:** Allure → GitHub Actions → GitHub Pages.

---

## 🛠 Stack

| Component | Technology |
|-----------|------------|
| 🐍 Language | Python 3.12+ |
| 🧪 Test runner | Pytest 7.4.3 + pytest-xdist 3.5.0 + pytest-rerunfailures 15.1 |
| 🌐 UI | Selenium 4.15.2 |
| 📊 Reporting | allure-pytest 2.13.2 |
| ⚙️ Config | python-dotenv, `BASE_URL` / `BROWSER` / `HEADLESS` / `LOCAL_LOG` |
| 🛡️ Types / hooks | mypy, pre-commit |
| ⚙️ CI/CD | GitHub Actions → Allure on Pages |
| 🔗 Stand | demo shop (URL in `.env` / Secrets as `BASE_URL`) |

---

## 🚀 Quick start

```bash
git clone https://github.com/aliaksandr-stanavy/ui-selenium-test-automation-framework.git
cd ui-selenium-test-automation-framework

python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix:    source .venv/bin/activate

pip install -r requirements.txt
# optional: make install-dev   # mypy + pre-commit hooks
copy .env.example .env   # or: cp .env.example .env
# set BASE_URL (and BROWSER / HEADLESS if needed)

make smoke
# or: pytest -m smoke -q
# with window: pytest -m smoke --headed
```

| Variable | Description |
|----------|-------------|
| `BASE_URL` | shop base URL (no trailing slash) |
| `BROWSER` | `chrome` (default) or `firefox` |
| `HEADLESS` | `true` (default) / `false` — show browser window |
| `LOCAL_LOG` | `true` → `logs/test-run.log` |

CI uses **GitHub Secrets**. Full guide: [quick-start](docs/en/quick-start.md) · Make & Allure: [local-run](docs/en/local-run.md).

---

## 📁 Layout

```text
ui-selenium-test-automation-framework/
├── pages/               # Page Objects + locators/
├── tests/               # scenarios
├── utils/               # EC, run_config, Allure env/attach
├── conftest.py          # driver + page fixtures
├── pytest.ini
├── pyproject.toml       # mypy
├── requirements.txt
├── requirements-dev.txt # mypy, pre-commit
├── Makefile
├── scripts/local/maintenance/  # clean.py — caches / Allure artifacts
├── .pre-commit-config.yaml
├── docs/
│   ├── README.md        # language switcher
│   ├── ru/              # documentation (RU)
│   └── en/              # documentation (EN)
├── .github/workflows/   # CI/CD
├── LICENSE
└── CHANGELOG.md
```

---

## 📚 Documentation

Canonical index: **[docs/en/index.md](docs/en/index.md)**. Navigation by task below.

### Documentation map

| If you need to... | Document | ⏱ Approx. time |
|---|---|---|
| **Run the tests** | [Quick start](docs/en/quick-start.md) | ~5 minutes |
| **Understand the code** | [Architecture](docs/en/architecture.md) | 15 minutes |
| **Pick a fixture** | [Fixtures reference](docs/en/fixtures-reference.md) | 10 minutes |
| **Learn product UI flows** | [BRD](docs/en/brd.md) | 10 minutes |
| **Check markers and expectations** | [QA requirements](docs/en/qa-requirements.md) | 10 minutes |
| **See all Make targets** | [Local run](docs/en/local-run.md) | 5 minutes |
| **Set up hooks / mypy** | [Pre-commit](docs/en/pre-commit.md) | 5 minutes |
| **Debug a red CI** | [CI/CD](docs/en/ci-cd.md) + [Test analysis](docs/en/test-analysis.md) | 15 minutes |
| **Fix a problem** | [Troubleshooting](docs/en/troubleshooting.md) | 5 minutes |

Changelog: [CHANGELOG.md](CHANGELOG.md).

---

## ✅ Coverage

| Area | Scenarios (~10 per page, ~33 total) |
|------|-------------------------------------|
| Category | listing, Desk / case-partial search, empty, resilience, sort by price, hover ATC, PDP, mobile products |
| Product | image, price, qty ± / direct / invalid, add to cart → toast, breadcrumb, Terms, mobile image |
| Cart | empty, item, continue shopping, toast URL, qty→total, remove, checkout on/off, reload, qty from PDP |

Markers: `pytest -m smoke`, `pytest -m critical`, `pytest -m negative`, `pytest -m regression`, `pytest -m mobile`.

---

## 📊 Allure Report

```bash
pytest --alluredir=allure-results
allure serve allure-results
# or: make allure
```

In CI the report is published to **GitHub Pages**:
[https://aliaksandr-stanavy.github.io/ui-selenium-test-automation-framework/](https://aliaksandr-stanavy.github.io/ui-selenium-test-automation-framework/)
Details: [local-run](docs/en/local-run.md), [ci-cd](docs/en/ci-cd.md).

---

## 👤 Author

This project was built while developing my expertise in **Full Stack QA** and is part of my public **GitHub portfolio**.
Its goal is to show modern approaches to UI frameworks, test organization, and CI/CD.

Feedback, suggestions, and professional conversation are welcome.

- 🌐 **GitHub Portfolio:** https://github.com/aliaksandr-stanavy
- 💼 **LinkedIn:** https://www.linkedin.com/in/aliaksandr-stanavy/

---
 
## 🏷️ Badges
 
| Badge | Meaning |
|-------|---------|
| Python | Supported Python version |
| Pytest | Test runner version |
| Selenium | WebDriver version |
| Allure | Report tool version |
| CI | GitHub Actions workflow status |
| Allure Report | Live Allure report on GitHub Pages |
| License | MIT license |
| GitHub | Author's GitHub profile |
 
---
 
## 📄 License
 
This project is distributed under the **MIT** license.
 
See [LICENSE](LICENSE) for details.
 
© 2026 Aliaksandr Stanavy
 
---
 
*Last updated: 2026-11-08*
