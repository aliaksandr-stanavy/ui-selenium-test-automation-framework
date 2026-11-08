# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-11-08

### Added
- Initial release of Selenium UI test automation framework for a demo shop (category / product / cart)
- Lean Page Object Model: `BasePage` + page classes; locators isolated under `pages/locators/`; asserts in `verify_*`
- Explicit waits only (no `time.sleep` / `implicitly_wait`); custom expected condition `text_to_be_not_empty`
- Pytest fixtures: function-scoped `driver`, `cart_page`, `category_page`, `product_page`
- Run config via env/CLI: `BASE_URL`, `BROWSER`, `HEADLESS`, `LOCAL_LOG` / `--headed` / `--browser` / `--local-log` (CLI > env)
- Suite ~33 test-IDs: search/sort, hover ATC, quantity boundaries, cart persistence, resilience to malformed input, mobile viewport smoke (`390×844`)
- Pytest markers: page (`cart` / `category` / `product`) + priority (`smoke` / `critical` / `medium` / `negative` / `regression`) + `mobile`
- Allure: steps; fail-only `page_url` / `screenshot` / `page_source` / `console_log`; auto `environment.properties`
- Parallel runs (`pytest-xdist`, `make parallel` / CI `-n 2`); flaky opt-in (`make rerun`; CI `--reruns 1`)
- CI/CD via GitHub Actions: mypy → pytest → Allure on GitHub Pages; Chrome full suite + Chrome/Firefox smoke matrix; Pages deploy on green `push` to `main`/`master` only
- `Makefile` for local runs; mypy + pre-commit hooks
- Local maintenance script `scripts/local/maintenance/clean.py` (`make clean` / `make clean-dry`)
- Bilingual documentation: `docs/ru/` and `docs/en/`

### Technologies
- Python 3.12+
- Pytest 7.4.3
- pytest-xdist 3.5.0
- pytest-rerunfailures 15.1
- Selenium 4.15.2
- allure-pytest 2.13.2
- python-dotenv 1.0.1
- mypy / pre-commit
- GitHub Actions
