# ui-selenium-test-automation-framework — quick pytest / Allure runners
#
# Requires: make (Git Bash / WSL / Chocolatey), Python venv, allure CLI
#
# Examples:
#   make help
#   make test
#   make critical
#   make cart
#   make headed
#   make run ARGS="--headed --browser firefox --local-log"
#   make marker M=smoke
#   make file F=tests/test_cart.py
#   make allure

.PHONY: help install install-dev test all lint mypy \
	pre-commit pre-commit-run pre-commit-install \
	smoke critical medium cart category product negative regression \
	headed firefox log parallel rerun mobile run \
	marker file failed last allure allure-gen clean clean-dry

PYTHON ?= python
PYTEST ?= $(PYTHON) -m pytest
PRE_COMMIT ?= $(PYTHON) -m pre_commit
ALLURE_DIR ?= allure-results
ALLURE_REPORT ?= allure-report
CLEAN_ARGS ?=

.DEFAULT_GOAL := help

help: ## Show available targets
	@echo Available targets:
	@echo   make install             - install dependencies from requirements.txt
	@echo   make install-dev         - install runtime + mypy/pre-commit + git hooks
	@echo   make lint                - run mypy
	@echo   make mypy                - alias for lint
	@echo   make pre-commit          - run all pre-commit hooks on all files
	@echo   make pre-commit-run      - alias for pre-commit
	@echo   make pre-commit-install  - install git hooks only
	@echo   make test                - run all tests
	@echo   make smoke               - only @pytest.mark.smoke
	@echo   make critical            - only @pytest.mark.critical
	@echo   make medium              - only @pytest.mark.medium
	@echo   make cart                - only @pytest.mark.cart
	@echo   make category            - only @pytest.mark.category
	@echo   make product             - only @pytest.mark.product
	@echo   make negative            - only @pytest.mark.negative
	@echo   make regression          - only @pytest.mark.regression
	@echo   make headed              - pytest --headed
	@echo   make firefox             - pytest --browser firefox
	@echo   make log                 - pytest --local-log
	@echo   make parallel            - pytest -n auto (pytest-xdist)
	@echo   make rerun               - pytest --reruns 1 --reruns-delay 1
	@echo   make mobile              - only @pytest.mark.mobile (390x844)
	@echo   make run ARGS="..."      - pytest with custom args
	@echo   make marker M=...        - custom marker     (make marker M=smoke)
	@echo   make file F=...          - specific file     (make file F=tests/test_cart.py)
	@echo   make failed              - rerun failed only (--lf)
	@echo   make last                - stop on first failure (-x)
	@echo   make allure              - generate and open Allure report
	@echo   make allure-gen          - generate report without serve
	@echo   make clean               - remove caches, logs, and Allure artifacts
	@echo   make clean-dry           - preview what make clean would delete

install: ## Install dependencies
	$(PYTHON) -m pip install -r requirements.txt

install-dev: install ## Install runtime + dev tooling
	$(PYTHON) -m pip install -r requirements-dev.txt
	$(PRE_COMMIT) install

lint: ## Run mypy type checks
	$(PYTHON) -m mypy

mypy: lint ## Alias for lint

pre-commit-install: ## Install pre-commit git hooks
	$(PRE_COMMIT) install

pre-commit-run: ## Run all pre-commit hooks on all files
	$(PRE_COMMIT) run --all-files

pre-commit: pre-commit-run ## Alias for pre-commit-run

test: ## Run all tests
	$(PYTEST)

all: test ## Alias for test

smoke: ## Smoke tests
	$(PYTEST) -m smoke

critical: ## Critical tests
	$(PYTEST) -m critical

medium: ## Medium-priority tests
	$(PYTEST) -m medium

cart: ## Cart page tests
	$(PYTEST) -m cart

category: ## Category page tests
	$(PYTEST) -m category

product: ## Product page tests
	$(PYTEST) -m product

negative: ## Negative / resilience tests
	$(PYTEST) -m negative

regression: ## Regression tests
	$(PYTEST) -m regression

headed: ## Show browser window
	$(PYTEST) --headed

firefox: ## Run with Firefox
	$(PYTEST) --browser firefox

log: ## Write local log file (logs/test-run.log)
	$(PYTEST) --local-log

parallel: ## Parallel run (pytest-xdist, auto worker count)
	$(PYTEST) -n auto

rerun: ## Run with one retry on failure
	$(PYTEST) --reruns 1 --reruns-delay 1

mobile: ## Mobile viewport smoke (~390x844)
	$(PYTEST) -m mobile

run: ## Custom pytest args: make run ARGS="--headed --browser firefox"
ifndef ARGS
	$(error Provide args: make run ARGS="--headed --browser firefox --local-log")
endif
	$(PYTEST) $(ARGS)

marker: ## Custom marker: make marker M=smoke
ifndef M
	$(error Provide a marker: make marker M=smoke)
endif
	$(PYTEST) -m "$(M)"

file: ## Specific file: make file F=tests/test_cart.py
ifndef F
	$(error Provide a file: make file F=tests/test_cart.py)
endif
	$(PYTEST) "$(F)"

failed: ## Rerun only failed tests
	$(PYTEST) --lf --last-failed-no-failures none

last: ## Stop on first failure
	$(PYTEST) -x

allure-gen: ## Generate Allure HTML report
	allure generate $(ALLURE_DIR) -o $(ALLURE_REPORT) --clean

allure: allure-gen ## Generate and open Allure report
	allure open $(ALLURE_REPORT)

clean-dry: ## Preview caches / Allure artifacts that would be removed
	$(PYTHON) scripts/local/maintenance/clean.py --dry-run $(CLEAN_ARGS)

clean: ## Remove pytest caches, logs, and Allure artifacts
	$(PYTHON) scripts/local/maintenance/clean.py --yes $(CLEAN_ARGS)
