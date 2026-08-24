import shutil
from os import name, system

from app.constants import Constants as C

_COLORS_ENABLED: bool = True
_CLEAR_SCREEN_ENABLED: bool = True
_HINTS_ENABLED: bool = True


def set_colors_enabled(enabled: bool) -> None:
    global _COLORS_ENABLED
    _COLORS_ENABLED = enabled


def set_clear_screen_enabled(enabled: bool) -> None:
    global _CLEAR_SCREEN_ENABLED
    _CLEAR_SCREEN_ENABLED = enabled


def set_hints_enabled(enabled: bool) -> None:
    global _HINTS_ENABLED
    _HINTS_ENABLED = enabled


def make_cyan(text: str) -> str:
    if _COLORS_ENABLED:
        return C.ANSI_CYAN + text + C.ANSI_RESET
    return text


def make_muted(text: str) -> str:
    if _COLORS_ENABLED:
        return C.ANSI_DIM + text + C.ANSI_RESET
    return text


def make_red(text: str) -> str:
    if _COLORS_ENABLED:
        return C.ANSI_RED + text + C.ANSI_RESET
    return text


def make_pink(text: str) -> str:
    if _COLORS_ENABLED:
        return C.ANSI_PINK + text + C.ANSI_RESET
    return text


def make_hint(text: str, danger: bool = False) -> str:
    if _HINTS_ENABLED:
        return make_red(text) if danger else make_cyan(text)
    return ""


def make_box(lines: list[str], title: str) -> str:
    content_width: int = max(len(line) for line in lines)
    result: str = ""
    result += f"╭─ {title} {'─' * (content_width - len(title) - 2)}─╮\n"
    for line in lines:
        result += f"│ {line.ljust(content_width)} |\n"
    result += f"╰{'─' * (content_width + 2)}╯"
    return result


def get_header(text: str, pink: bool = False) -> str:
    width: int = shutil.get_terminal_size().columns
    if width <= 0:
        width = C.DEFAULT_TERMINAL_WIDTH
    padding: int = max(0, width - len(text) - 2)

    return (
        "=" * (padding // 2)
        + " "
        + (make_cyan(text) if not pink else make_pink(text))
        + " "
        + "=" * (padding - padding // 2)
    )


def build_view(header: str, body: str, hint: str) -> str:
    parts = [header, body]
    if hint:
        parts.append(hint)
    return "\n\n".join(part for part in parts if part) + "\n"


def clear_screen() -> None:
    if not _CLEAR_SCREEN_ENABLED:
        return
    if name == "nt":
        system("cls")
    else:
        system("clear")
