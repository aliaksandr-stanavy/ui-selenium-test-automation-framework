# Быстрый старт

Запуск UI-тестов за ~5 минут.

**Язык:** Русский · [English](../en/quick-start.md)

## 1. Клонирование и venv

```bash
git clone https://github.com/aliaksandr-stanavy/ui-selenium-test-automation-framework.git
cd ui-selenium-test-automation-framework

python -m venv .venv
# Windows:
.venv\Scripts\activate
# Unix:
source .venv/bin/activate

pip install -r requirements.txt
# опционально (mypy + pre-commit): make install-dev
```

Нужны Python 3.12+ и браузер Chrome (или Firefox). Драйвер подтягивает Selenium Manager.

## 2. Конфиг `.env`

```bash
copy .env.example .env   # Windows
# cp .env.example .env   # Unix
```

| Переменная | Пример | Обязательно |
|------------|--------|-------------|
| `BASE_URL` | `<your-stand-url>` | да |
| `BROWSER` | `chrome` | нет (default `chrome`) |
| `HEADLESS` | `true` | нет (default `true`) |
| `LOCAL_LOG` | `false` | нет |

Подставьте URL вашего стенда. В публичных примерах — placeholder `https://shop.example.com`.

С окном браузера: `pytest -m smoke --headed` (или `HEADLESS=false`).

## 3. Прогон

```bash
make smoke
# или:
pytest -m smoke -q
```

Полный suite (~33 тестов): `make all` / `pytest`.

Другие срезы: `make critical`, `make negative`, `make regression`, `make mobile` — см. [local-run](local-run.md).

Карта сценариев: [qa-requirements](qa-requirements.md).

## 4. Allure (локально)

```bash
pytest
allure serve allure-results
```

Нужен [Allure Commandline](https://allurereport.org/docs/install/) и Java runtime (JRE 8+) в `PATH` — сам CLI написан на Java.

Дальше: [architecture](architecture.md) · [local-run](local-run.md) · [troubleshooting](troubleshooting.md).

---
 
*Last updated: 2026-11-08*
