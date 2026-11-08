"""Fail-only Allure attachments for UI diagnostics."""

from __future__ import annotations

import logging
from typing import Any

import allure
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver

logger = logging.getLogger(__name__)

# Keep Allure HTML attachments bounded for Odoo-like pages with heavy inline assets.
PAGE_SOURCE_MAX_BYTES = 400_000


def attach_page_url(driver: WebDriver) -> None:
    allure.attach(
        driver.current_url,
        name="page_url",
        attachment_type=allure.attachment_type.TEXT,
    )


def attach_screenshot(driver: WebDriver) -> None:
    allure.attach(
        driver.get_screenshot_as_png(),
        name="screenshot",
        attachment_type=allure.attachment_type.PNG,
    )


def attach_page_source(driver: WebDriver) -> None:
    source = driver.page_source or ""
    encoded = source.encode("utf-8", errors="replace")
    total = len(encoded)
    if total > PAGE_SOURCE_MAX_BYTES:
        truncated = encoded[:PAGE_SOURCE_MAX_BYTES].decode(
            "utf-8", errors="replace"
        )
        source = (
            f"{truncated}\n"
            f"...(truncated, {total} bytes total)"
        )
    allure.attach(
        source,
        name="page_source",
        attachment_type=allure.attachment_type.HTML,
    )


def _format_browser_logs(entries: list[dict[str, Any]]) -> str:
    if not entries:
        return "<no browser logs>"
    lines: list[str] = []
    for entry in entries:
        level = entry.get("level", "?")
        message = entry.get("message", "")
        timestamp = entry.get("timestamp", "")
        lines.append(f"[{level}] {timestamp} {message}")
    return "\n".join(lines)


def attach_console_log(driver: WebDriver) -> None:
    browser = (getattr(driver, "name", "") or "").lower()
    get_log = getattr(driver, "get_log", None)
    if not callable(get_log):
        allure.attach(
            "console logs not available for this browser",
            name="console_log",
            attachment_type=allure.attachment_type.TEXT,
        )
        return

    try:
        entries = get_log("browser")
    except WebDriverException:
        text = (
            "console logs not available for firefox"
            if "firefox" in browser
            else "console logs not available for this browser"
        )
        allure.attach(
            text,
            name="console_log",
            attachment_type=allure.attachment_type.TEXT,
        )
        return

    allure.attach(
        _format_browser_logs(list(entries)),
        name="console_log",
        attachment_type=allure.attachment_type.TEXT,
    )


def attach_failure_artifacts(driver: WebDriver) -> None:
    """Attach url → screenshot → page_source → console; each independently."""
    for name, attach in (
        ("page_url", attach_page_url),
        ("screenshot", attach_screenshot),
        ("page_source", attach_page_source),
        ("console_log", attach_console_log),
    ):
        try:
            attach(driver)
        except Exception:
            logger.debug(
                "Failed to attach %s to Allure", name, exc_info=True
            )
