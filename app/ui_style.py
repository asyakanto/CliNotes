import shutil
from dataclasses import dataclass
from os import name, system

from app.app import NotesApp
from app.constants import Constants as C


@dataclass
class StyleConfig:
    colors: bool = True
    clear_screen: bool = True
    hints: bool = True


def make_cyan(text: str, config: StyleConfig) -> str:
    if config.colors:
        return C.ANSI_CYAN + text + C.ANSI_RESET
    return text


def make_muted(text: str, config: StyleConfig) -> str:
    if config.colors:
        return C.ANSI_DIM + text + C.ANSI_RESET
    return text


def make_red(text: str, config: StyleConfig) -> str:
    if config.colors:
        return C.ANSI_RED + text + C.ANSI_RESET
    return text


def make_pink(text: str, config: StyleConfig) -> str:
    if config.colors:
        return C.ANSI_PINK + text + C.ANSI_RESET
    return text


def make_hint(text: str, config: StyleConfig, danger: bool = False) -> str:
    if config.hints:
        return make_red(text, config) if danger else make_cyan(text, config)
    return ""


def make_box(lines: list[str], title: str) -> str:
    content_width: int = max(len(line) for line in lines)
    result: str = ""
    result += f"╭─ {title} {'─' * (content_width - len(title) - 2)}─╮\n"
    for line in lines:
        result += f"│ {line.ljust(content_width)} |\n"
    result += f"╰{'─' * (content_width + 2)}╯"
    return result


def get_header(text: str, config: StyleConfig, pink: bool = False) -> str:
    width: int = shutil.get_terminal_size().columns
    if width <= 0:
        width = C.DEFAULT_TERMINAL_WIDTH
    padding: int = max(0, width - len(text) - 2)

    return (
        "=" * (padding // 2)
        + " "
        + (make_cyan(text, config) if not pink else make_pink(text, config))
        + " "
        + "=" * (padding - padding // 2)
    )


def build_view(header: str, body: str, hint: str) -> str:
    parts = [header, body]
    if hint:
        parts.append(hint)
    return "\n\n".join(part for part in parts if part) + "\n"


def clear_screen(config: StyleConfig) -> None:
    if not config.clear_screen:
        return
    if name == "nt":
        system("cls")
    else:
        system("clear")


def apply_settings(app: NotesApp, config: StyleConfig, key: str | None = None) -> None:
    if key is None or key == C.SETTING_USE_COLORS:
        config.colors = app.settings.get_bool_value(C.SETTING_USE_COLORS)

    if key is None or key == C.SETTING_USE_CLEAR_SCREEN:
        config.clear_screen = app.settings.get_bool_value(C.SETTING_USE_CLEAR_SCREEN)
    if key is None or key == C.SETTING_USE_HINTS:
        config.hints = app.settings.get_bool_value(C.SETTING_USE_HINTS)
    if key is None or (
        key in C.TAG_PREFIX_SETTINGS
        or key == C.SETTING_AUTO_DATE_TAG
        or key == C.SETTING_AUTO_SYNC_TAGS
    ):
        app.sync_tags_if_enabled()
    if key is None or key == C.SETTING_NOTES_PATH:
        app.apply_notes_path()
    if key is None or key == C.SETTING_LOG_LEVEL:
        app.apply_log_level()
