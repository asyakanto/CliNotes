"""Styling helpers: ANSI colors, headers and view layout."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from os import name
from typing import TYPE_CHECKING

from app.constants import Constants

if TYPE_CHECKING:
    from app.app import NotesApp


@dataclass
class StyleConfig:
    """User-configurable display options: colors, clearing and hints."""

    colors: bool = True
    clear_screen: bool = True
    hints: bool = True


def make_cyan(text: str, config: StyleConfig) -> str:
    """Wrap text in cyan ANSI colors when enabled."""
    if config.colors:
        return Constants.ANSI_CYAN + text + Constants.ANSI_RESET
    return text


def make_muted(text: str, config: StyleConfig) -> str:
    """Wrap text in dim ANSI colors when enabled."""
    if config.colors:
        return Constants.ANSI_DIM + text + Constants.ANSI_RESET
    return text


def make_red(text: str, config: StyleConfig) -> str:
    """Wrap text in red ANSI colors when enabled."""
    if config.colors:
        return Constants.ANSI_RED + text + Constants.ANSI_RESET
    return text


def make_pink(text: str, config: StyleConfig) -> str:
    """Wrap text in pink ANSI colors when enabled."""
    if config.colors:
        return Constants.ANSI_PINK + text + Constants.ANSI_RESET
    return text


def make_hint(text: str, config: StyleConfig, *, danger: bool = False) -> str:
    """Return styled hint text, or empty when hints are off."""
    if config.hints:
        return make_red(text, config) if danger else make_cyan(text, config)
    return ""


def make_box(lines: list[str], title: str) -> str:
    """Render lines inside a box with a title."""
    content_width: int = max(len(line) for line in lines)
    result: str = ""
    result += f"╭─ {title} {'─' * (content_width - len(title) - 2)}─╮\n"
    for line in lines:
        result += f"│ {line.ljust(content_width)} |\n"
    result += f"╰{'─' * (content_width + 2)}╯"
    return result


def get_header(text: str, config: StyleConfig, *, pink: bool = False) -> str:
    """Build a centered header line spanning the terminal width."""
    width: int = shutil.get_terminal_size().columns
    if width <= 0:
        width = Constants.DEFAULT_TERMINAL_WIDTH
    padding: int = max(0, width - len(text) - 2)

    return (
        "=" * (padding // 2)
        + " "
        + (make_cyan(text, config) if not pink else make_pink(text, config))
        + " "
        + "=" * (padding - padding // 2)
    )


def build_view(header: str, body: str, hint: str) -> str:
    """Join header, body and hint into a single view string."""
    parts = [header, body]
    if hint:
        parts.append(hint)
    return "\n\n".join(part for part in parts if part) + "\n"


def clear_screen(config: StyleConfig) -> None:
    """Clear the terminal when enabled."""
    if not config.clear_screen:
        return
    if name == "nt":
        subprocess.run(["cls"], check=False)  # noqa: S607
    else:
        subprocess.run(["clear"], check=False)  # noqa: S607


def apply_settings(
    app: NotesApp, config: StyleConfig, key: str | None = None, *, start: bool = False
) -> None:
    """Sync the style config with the application settings."""
    if key is None or key == Constants.SETTING_USE_COLORS:
        config.colors = app.settings.get_bool_value(Constants.SETTING_USE_COLORS)

    if key is None or key == Constants.SETTING_USE_CLEAR_SCREEN:
        config.clear_screen = app.settings.get_bool_value(
            Constants.SETTING_USE_CLEAR_SCREEN
        )
    if key is None or key == Constants.SETTING_USE_HINTS:
        config.hints = app.settings.get_bool_value(Constants.SETTING_USE_HINTS)
    if key is None or (
        key
        in set(Constants.TAG_PREFIX_SETTINGS)
        | {Constants.SETTING_AUTO_DATE_TAG, Constants.SETTING_AUTO_SYNC_TAGS}
    ):
        app.sync_tags_if_enabled()
    if (key is None or key == Constants.SETTING_NOTES_PATH) and not start:
        app.apply_notes_path()
    if key is None or key == Constants.SETTING_LOG_LEVEL:
        app.apply_log_level()
