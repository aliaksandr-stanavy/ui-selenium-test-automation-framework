"""Run-time config: browser / headless / local logging (CLI > env > default)."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from _pytest.config import Config

SUPPORTED_BROWSERS = frozenset({"chrome", "firefox"})


def parse_bool(value: Optional[str]) -> Optional[bool]:
    """Parse common truthy/falsy strings; None if unset or unrecognized."""
    if value is None:
        return None
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    return None


def _cli_option(config: Optional["Config"], name: str) -> object:
    if config is None:
        return None
    try:
        return config.getoption(name)
    except (ValueError, AttributeError):
        return None


def get_browser(config: Optional["Config"] = None) -> str:
    """Resolve browser: --browser > BROWSER env > chrome."""
    cli = _cli_option(config, "--browser")
    cli_str = cli if isinstance(cli, str) else None
    raw = (cli_str or os.getenv("BROWSER") or "chrome").strip().lower()
    if raw not in SUPPORTED_BROWSERS:
        raise ValueError(
            f"Unsupported browser: {raw!r}. "
            f"Use BROWSER=chrome|firefox or --browser chrome|firefox."
        )
    return raw


def is_headless(config: Optional[Config] = None) -> bool:
    """Resolve headless: --headed/--headless > HEADLESS env > True."""
    headed = bool(_cli_option(config, "--headed"))
    headless_flag = bool(_cli_option(config, "--headless"))
    if headed and headless_flag:
        raise ValueError("Use either --headed or --headless, not both.")
    if headed:
        return False
    if headless_flag:
        return True
    env = parse_bool(os.getenv("HEADLESS"))
    if env is not None:
        return env
    return True


def is_local_log(config: Optional[Config] = None) -> bool:
    """Resolve local log: --local-log/--no-local-log > LOCAL_LOG env > False."""
    on = bool(_cli_option(config, "--local-log"))
    off = bool(_cli_option(config, "--no-local-log"))
    if on and off:
        raise ValueError("Use either --local-log or --no-local-log, not both.")
    if on:
        return True
    if off:
        return False
    env = parse_bool(os.getenv("LOCAL_LOG"))
    if env is not None:
        return env
    return False


def get_log_level(config: Optional[Config] = None) -> str:
    """Log level from LOG_LEVEL env only (default INFO)."""
    del config  # reserved for future CLI; level stays env-only by design
    return (os.getenv("LOG_LEVEL") or "INFO").strip().upper() or "INFO"
