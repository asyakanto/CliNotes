"""Input helpers for the CLI: prompts, pause and confirmations."""

from __future__ import annotations

from typing import TYPE_CHECKING

from prompt_toolkit import prompt

from app.constants import Constants
from app.ui_style import make_cyan, make_red

if TYPE_CHECKING:
    from app.app import NotesApp
    from app.ui_style import StyleConfig


def read_input(
    *, lowercase: bool = True, prompt_default_text: str | None = None
) -> str:
    """Read a single line from the user, optionally lowercased."""
    response: str
    if prompt_default_text is None:
        response = input(Constants.UI_PROMPT).strip()
    else:
        response = prompt(default=prompt_default_text).strip()
    print()  # noqa: T201
    return response.lower() if lowercase else response


def pause(message: str, style_config: StyleConfig) -> None:
    """Show a message and wait for the user to press Enter."""
    print()  # noqa: T201
    input(make_red(message, style_config))


def prompt_input(
    hint: str,
    style_config: StyleConfig,
    *,
    lowercase: bool = True,
    prompt_default_text: str | None = None,
    danger: bool = False,
) -> str:
    """Show a styled hint and read a user input."""
    print(  # noqa: T201
        f"{make_red(hint, style_config) if danger else make_cyan(hint, style_config)}\n"
    )
    return read_input(lowercase=lowercase, prompt_default_text=prompt_default_text)


def confirm(
    app: NotesApp,
    setting_key: str,
    message: str,
    style_config: StyleConfig,
    *,
    danger: bool = False,
) -> bool:
    """Ask a yes/no question, respecting the confirm setting."""
    return (
        not app.settings.get_bool_value(setting_key)
        or prompt_input(message, style_config, danger=danger) == "y"
    )
