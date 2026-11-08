"""Write Allure environment.properties for the Environment report tab."""

from __future__ import annotations

import logging
import platform
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from pages.base_page import BasePage
from utils.run_config import get_browser, is_headless, is_local_log

if TYPE_CHECKING:
    from _pytest.config import Config

logger = logging.getLogger(__name__)


def build_environment(config: "Config") -> dict[str, str]:
    """Collect flat key=value pairs for Allure Environment."""
    return {
        "Browser": get_browser(config),
        "Headless": str(is_headless(config)).lower(),
        "LocalLog": str(is_local_log(config)).lower(),
        "BaseUrl": BasePage.base_url,
        "Python": sys.version.split()[0],
        "OS": platform.platform(),
    }


def write_environment_properties(config: "Config") -> Optional[Path]:
    """Write environment.properties into --alluredir; skip on xdist workers.

    Call from pytest_sessionfinish on the controller: under xdist, workers may
    still run AllureFileLogger(clean=True) after the controller's sessionstart,
    which would wipe a file written too early.
    """
    if hasattr(config, "workerinput"):
        return None  # write once from the controller process only

    report_dir = getattr(config.option, "allure_report_dir", None)
    if not report_dir:
        return None

    try:
        env = build_environment(config)
        target = Path(report_dir)
        target.mkdir(parents=True, exist_ok=True)
        path = target / "environment.properties"
        lines = [f"{key}={value}" for key, value in env.items()]
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path
    except Exception:
        logger.warning(
            "Failed to write Allure environment.properties",
            exc_info=True,
        )
        return None
