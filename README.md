# 🧪 Shop UI — Test Automation (Selenium)

**Язык:** Русский · [English](README.en.md)

[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Pytest-7.4.3-0A9EDC?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.15.2-43B02A?logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![Allure](https://img.shields.io/badge/Allure-2.13.2-purple?logo=allure&logoColor=white)](https://allurereport.org/)
[![CI](https://github.com/aliaksandr-stanavy/ui-selenium-test-automation-framework/actions/workflows/ui-tests.yml/badge.svg)](https://github.com/aliaksandr-stanavy/ui-selenium-test-automation-framework/actions/workflows/ui-tests.yml)
[![Allure Report](https://img.shields.io/badge/Allure-GitHub%20Pages-orange?logo=allure&logoColor=white)](https://aliaksandr-stanavy.github.io/ui-selenium-test-automation-framework/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-aliaksandr--stanavy-181717?logo=github&logoColor=white)](https://github.com/aliaksandr-stanavy)

**UI test automation framework** для демо-магазина на Python + Pytest + Selenium + Allure (Page Object Model).

> Этот проект — **демонстрация промышленного подхода** к UI-тестированию: lean POM, стабильные waits, risk-based сценарии, Allure и полноценный CI/CD.
>
> **Portfolio project** — demonstrating production-grade UI automation: lean POM, explicit waits, Allure + Pages, cross-browser CI.

| Старт | Документация |
|-------|----------------|
| [Быстрый старт](docs/ru/quick-start.md) (~5 мин) | [Оглавление RU](docs/ru/index.md) · [EN](docs/en/index.md) · [языки](docs/README.md) |

---

## 📖 О проекте

Фреймворк показывает, как выстроить инфраструктуру UI-автоматизации с акцентом на **надёжность, поддерживаемость и прозрачность результатов**.

**Ключевые возможности:**
- 🏗️ **Page Object Model** — `BasePage` → страницы, локаторы отдельно в `pages/locators/`.
- 📊 **Allure-отчёты** — шаги; при падении: screenshot, URL, page_source, console; вкладка Environment (browser, BASE_URL, OS).
- 🏷️ **Маркеры** — page (`cart` / `category` / `product`) + priority (`smoke` / `critical` / `medium` / `negative` / `regression`) + `mobile` viewport.
- ⏱️ **Explicit waits** — без `time.sleep` и без `implicitly_wait`; кастомный expected condition.
- 🌐 **Браузер через env/CLI** — `BROWSER=chrome|firefox`, `HEADLESS`, опционально `--headed` / `--local-log`.
- 📱 **Mobile viewport smoke** — `make mobile` / `-m mobile` на 390×844 (desktop sort/`d-lg-*` не входят).
- 🧩 **CI cross-browser smoke** — matrix Chrome + Firefox на `-m smoke`; полный regress / Pages — только Chrome.
- ⚡ **Parallel runs** — `pytest-xdist` (`make parallel` / CI `-n 2`); function-scoped driver = изоляция сессий.
- 🔁 **Flaky reruns** — в CI `--reruns 1`; локально opt-in (`make rerun`), default без retry.
- ⚙️ **CI/CD** — GitHub Actions с публикацией отчёта на GitHub Pages.
- 🛡️ **Статический анализ** — mypy + pre-commit хуки в CI.

### 🔥 Что именно демонстрирую

- **Lean POM:** asserts только в `verify_*` на page objects, без оверинжиниринга.
- **Стабильную синхронизацию:** explicit waits + `text_to_be_not_empty`, boundary waits без ложных positive.
- **Risk-based UI-flows:** поиск/sort, hover ATC, границы quantity, корзина, persistence, resilience к malformed input.
- **Качество кода:** типизация page layer (mypy), pre-commit в CI.
- **Полный контур отчёта:** Allure → GitHub Actions → GitHub Pages.

---

## 🛠 Стек

| Компонент | Технология |
|-----------|------------|
| 🐍 Язык | Python 3.12+ |
| 🧪 Тест-раннер | Pytest 7.4.3 + pytest-xdist 3.5.0 + pytest-rerunfailures 15.1 |
| 🌐 UI | Selenium 4.15.2 |
| 📊 Отчёты | allure-pytest 2.13.2 |
| ⚙️ Конфиг | python-dotenv, `BASE_URL` / `BROWSER` / `HEADLESS` / `LOCAL_LOG` |
| 🛡️ Типы / хуки | mypy, pre-commit |
| ⚙️ CI/CD | GitHub Actions → Allure на Pages |
| 🔗 Стенд | демо-магазин (URL в `.env` / Secrets как `BASE_URL`) |

---

## 🚀 Быстрый старт

```bash
git clone https://github.com/aliaksandr-stanavy/ui-selenium-test-automation-framework.git
cd ui-selenium-test-automation-framework

python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix:    source .venv/bin/activate

pip install -r requirements.txt
# optional: make install-dev   # mypy + pre-commit hooks
copy .env.example .env   # или: cp .env.example .env
# заполните BASE_URL (и при необходимости BROWSER / HEADLESS)

make smoke
# или: pytest -m smoke -q
# с окном: pytest -m smoke --headed
```

| Переменная | Описание |
|------------|----------|
| `BASE_URL` | базовый URL магазина (без trailing slash) |
| `BROWSER` | `chrome` (по умолчанию) или `firefox` |
| `HEADLESS` | `true` (default) / `false` — показать окно |
| `LOCAL_LOG` | `true` → `logs/test-run.log` |

В CI — **GitHub Secrets**. Полный гайд: [quick-start](docs/ru/quick-start.md) · Make и Allure: [local-run](docs/ru/local-run.md).

---

## 📁 Структура

```text
ui-selenium-test-automation-framework/
├── pages/               # Page Objects + locators/
├── tests/               # сценарии
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
│   ├── README.md        # навигатор языков
│   ├── ru/              # документация (RU)
│   └── en/              # документация (EN)
├── .github/workflows/   # CI/CD
├── LICENSE
└── CHANGELOG.md
```

---

## 📚 Документация

Полное оглавление: **[docs/ru/index.md](docs/ru/index.md)**. Ниже — навигация по документации.

### Навигация по документации

| Если вам нужно... | Документ | ⏱ Примерное время |
|---|---|---|
| **Запустить тесты** | [Быстрый старт](docs/ru/quick-start.md) | ~5 минут |
| **Понять устройство кода** | [Архитектура](docs/ru/architecture.md) | 15 минут |
| **Выбрать фикстуру** | [Справочник фикстур](docs/ru/fixtures-reference.md) | 10 минут |
| **Узнать UI-flows продукта** | [BRD](docs/ru/brd.md) | 10 минут |
| **Проверить маркеры и ожидания** | [QA-требования](docs/ru/qa-requirements.md) | 10 минут |
| **Узнать все Make-команды** | [Локальный запуск](docs/ru/local-run.md) | 5 минут |
| **Настроить хуки / mypy** | [Pre-commit](docs/ru/pre-commit.md) | 5 минут |
| **Разобрать красный CI** | [CI/CD](docs/ru/ci-cd.md) + [Анализ результатов](docs/ru/test-analysis.md) | 15 минут |
| **Решить проблему** | [Troubleshooting](docs/ru/troubleshooting.md) | 5 минут |

История изменений: [CHANGELOG.md](CHANGELOG.md).

---

## ✅ Что покрыто

| Область | Сценарии (~10 на страницу, ~33 всего) |
|---------|----------------------------------------|
| Category | список, поиск Desk / case-partial, empty, resilience, sort по цене, hover ATC, PDP, mobile products |
| Product | изображение, цена, qty ± / direct / invalid, add to cart → toast, breadcrumb, Terms, mobile image |
| Cart | empty, item, continue shopping, toast URL, qty→total, remove, checkout on/off, reload, qty с PDP |

Маркеры: `pytest -m smoke`, `pytest -m critical`, `pytest -m negative`, `pytest -m regression`, `pytest -m mobile`.

---

## 📊 Allure Report

```bash
pytest --alluredir=allure-results
allure serve allure-results
# или: make allure
```

В CI отчёт публикуется на **GitHub Pages**:
[https://aliaksandr-stanavy.github.io/ui-selenium-test-automation-framework/](https://aliaksandr-stanavy.github.io/ui-selenium-test-automation-framework/)
Подробнее: [local-run](docs/ru/local-run.md), [ci-cd](docs/ru/ci-cd.md).

---

## 👤 Автор

Этот проект создан в рамках развития моей экспертизы в **Full Stack QA** и является частью моего публичного **GitHub-портфолио**.
Его цель — показать современные подходы к построению UI-фреймворков, организации тестов и CI/CD.

Буду рад обратной связи, предложениям и профессиональному общению.

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
 
## 📄 Лицензия
 
Проект распространяется по лицензии **MIT**.
 
Подробности см. в файле [LICENSE](LICENSE).
 
© 2026 Aliaksandr Stanavy
 
---
 
*Last updated: 2026-11-08*
