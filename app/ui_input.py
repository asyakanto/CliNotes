from prompt_toolkit import prompt

from app.app import NotesApp
from app.constants import Constants as C
from app.ui_style import make_cyan, make_red


def read_input(lowercase: bool = True, prompt_default_text: str | None = None) -> str:
    response: str
    if prompt_default_text is None:
        response = input(C.UI_PROMPT).strip()
    else:
        response = prompt(default=prompt_default_text).strip()
    print()
    return response.lower() if lowercase else response


def pause(message: str) -> None:
    print()
    input(make_red(message))


def prompt_input(
    hint: str,
    lowercase: bool = True,
    prompt_default_text: str | None = None,
    danger: bool = False,
) -> str:

    print(f"{make_red(hint) if danger else make_cyan(hint)}\n")
    return read_input(lowercase=lowercase, prompt_default_text=prompt_default_text)


def confirm(
    app: NotesApp, setting_key: str, message: str, danger: bool = False
) -> bool:
    return (
        not app.settings.get_bool_value(setting_key)
        or prompt_input(message, danger=danger) == "y"
    )
