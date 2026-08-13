from __future__ import annotations

import logging
import shutil
from datetime import datetime, timedelta
from os import name, system
from typing import TYPE_CHECKING

from prompt_toolkit import prompt

from app.constants import Constants as C
from app.models import get_date, get_local_now
from app.search import search_help

if TYPE_CHECKING:
    from app.app import NotesApp
    from app.models import Note
    from app.settings import Setting

logger = logging.getLogger(__name__)


def clear_screen() -> None:
    if name == "nt":
        system("cls")
    else:
        system("clear")


def open_note(app: NotesApp, note: Note) -> None:
    while True:
        clear_screen()
        print(show_note(note, app))
        action: C.ACTION_TYPE = note_interface(note)

        if action == C.ACTION_QUIT:
            break
        elif action == C.ACTION_ARCHIVE:
            app.archive_note(note)
        elif action == C.ACTION_CHANGE_TITLE:
            new_title: str = prompt_input(
                hint="New title", prompt_default_text=note.title, lowercase=False
            )
            app.edit_note(note, new_title, note.text)
        elif action == C.ACTION_CHANGE_TEXT:
            new_text: str = prompt_input(
                hint="New text", prompt_default_text=note.text, lowercase=False
            )
            app.edit_note(note, note.title, new_text)
        elif action == C.ACTION_UNKNOWN:
            pause("Wrong action")
        elif action == C.ACTION_RESTORE:
            app.restore_note(note)
        elif (
            action == C.ACTION_DELETE
            and prompt_input("Delete this note? (y/n)", danger=True) == "y"
        ):
            app.delete_note(note)
            break


def make_cyan(text: str) -> str:
    return C.ANSI_CYAN + text + C.ANSI_RESET


def make_muted(text: str) -> str:
    return C.ANSI_DIM + text + C.ANSI_RESET


def make_red(text: str) -> str:
    return C.ANSI_RED + text + C.ANSI_RESET


def show_note(note: Note, app: NotesApp) -> str:
    result: str = ""
    result += get_header(note.title)
    if note.archived:
        deleting_at: str
        try:
            deleting_at = get_date(
                datetime.strptime(
                    note.archived_at,
                    C.DATE_FORMAT_STORAGE,
                ).replace(tzinfo=get_local_now().tzinfo)
                + timedelta(days=C.AUTO_DELETE_DAYS),
                app.settings.date_pattern(),
            )
        except ValueError:
            deleting_at = "unknown date"
        result += make_red(f"ARCHIVED: note will be deleted at {deleting_at}" + "\n")
    result += make_muted(str(note.id) + " #: " + ", ".join(note.tags)) + "\n"
    result += "\n"
    result += note.text + "\n"
    result += "\n"
    if not note.archived:
        result += make_cyan(
            f"Choose action: {C.KEY_QUIT} - quit; {C.KEY_ARCHIVE} - archive note; {C.KEY_EDIT} - edit note"
            + "\n"
        )
    else:
        result += make_cyan(
            f"Choose action: {C.KEY_QUIT} - quit; {C.KEY_RESTORE} - restore note; {C.KEY_DELETE} - delete note"
            + "\n"
        )
    return result


def note_interface(note: Note) -> C.ACTION_TYPE:
    mode: str
    if not note.archived:
        mode = read_input()
        if mode == C.KEY_QUIT:
            return C.ACTION_QUIT
        elif mode == C.KEY_ARCHIVE:
            return C.ACTION_ARCHIVE
        elif mode == C.KEY_EDIT:
            editing_mode: str = prompt_input(
                hint=f"Edit: {C.KEY_EDIT_TITLE} - title, {C.KEY_EDIT_TEXT} - text"
            )
            if editing_mode == C.KEY_EDIT_TITLE:
                return C.ACTION_CHANGE_TITLE
            if editing_mode == C.KEY_EDIT_TEXT:
                return C.ACTION_CHANGE_TEXT
        return C.ACTION_UNKNOWN
    else:
        mode = read_input()
        if mode == C.KEY_QUIT:
            return C.ACTION_QUIT
        elif mode == C.KEY_RESTORE:
            return C.ACTION_RESTORE
        elif mode == C.KEY_DELETE:
            return C.ACTION_DELETE
        return C.ACTION_UNKNOWN


def get_visible_notes(notes: list[Note], display_archive: bool) -> list[Note]:
    if display_archive:
        return notes
    notes_list: list[Note] = []
    for note in notes:
        if not note.archived:
            notes_list.append(note)

    return notes_list


def display_notes(notes: list[Note]) -> str:
    if len(notes) != 0:
        lines: list[str] = []
        for note in notes:
            if not note.archived:
                lines.append(f"#{note.id} {note.title}")
            else:
                lines.append(make_muted(f"#{note.id} {note.title}"))
        return "\n".join(lines) + "\n"
    return make_muted(f"No notes yet — press {C.KEY_CREATE} to create \n")


def show_main_menu(app: NotesApp) -> str:
    result: str = ""
    visible_notes: list[Note] = get_visible_notes(
        app.notes, bool(app.settings.get_value(C.SETTING_SHOW_ARCHIVED))
    )
    result += get_header(
        f"CliNotes: {get_date(get_local_now(), app.settings.date_pattern())} · {len(visible_notes)} {'notes' if len(visible_notes) != 1 and len(visible_notes) != 0 else 'note'}"
    )
    result += "\n"
    result += get_notifications(app)

    result += display_notes(visible_notes) + "\n"

    result += make_cyan(
        "Actions: {ID}"
        + f" - open note; {C.KEY_QUIT} - quit; {C.KEY_CREATE} - create; {C.KEY_SEARCH} - search; {C.KEY_TOGGLE_ARCHIVED} - show archived; {C.KEY_SETTINGS} - settings"
        + "\n"
    )

    return result


def main_interface() -> str:

    mode = read_input()

    return mode


def get_notifications(app: NotesApp) -> str:
    if not app._notifications:
        return ""

    result: str = ""

    for notification in app.pop_notifications():
        result += make_red("[!] " + notification + "\n")
    return result + "\n"


def show_settings_categories(app: NotesApp) -> str:
    result: str = ""
    result += get_header("Settings") + "\n"

    groups: list[str] = app.settings.groups()
    for i, group in enumerate(groups):
        result += f"{i} - {group}\n"
    result += "\n" + make_cyan(
        "Actions: {ID} - open category; " + f"{C.KEY_SEARCH_QUIT} - quit"
    )
    return result


def settings_interface(app: NotesApp) -> None:
    groups = app.settings.groups()
    while True:
        clear_screen()
        print(show_settings_categories(app))
        action: str = read_input()
        if action == C.KEY_SEARCH_QUIT:
            return
        elif action.isdigit() and "." not in action:
            if 0 <= int(action) < len(groups):
                settings_group_interface(app, groups[int(action)])
            else:
                pause("Wrong ID")

        else:
            pause("Wrong action")


def show_settings_group(
    app: NotesApp, group_name: str, group_settings: list[Setting]
) -> str:
    result = ""
    result += get_header(group_name) + "\n"
    for i, setting in enumerate(group_settings):
        value: str = ""
        if type(setting.value) == bool:
            if setting.value:
                value = "on"
            else:
                value = "off"
        else:
            value = str(setting.value)
        result += str(i) + " " + setting.label + " " + make_cyan(value) + "\n"
    result += "\n" + make_cyan(
        "Actions: {ID} - change setting; " + f"{C.KEY_SEARCH_QUIT} - quit"
    )
    return result


def settings_group_interface(app: NotesApp, group: str) -> None:
    group_settings: list[Setting] = app.settings.settings_in_group(group)
    while True:
        clear_screen()
        print(show_settings_group(app, group, group_settings))
        action: str = read_input()
        if action == C.KEY_SEARCH_QUIT:
            app.save_settings()
            logger.info("Settings changed and saved successfully")
            return
        elif action.isdigit() and "." not in action:
            if 0 <= int(action) < len(group_settings):
                edit_setting(app, group_settings[int(action)])
            else:
                pause("Wrong ID")

        else:
            pause("Wrong action")


def edit_setting(app: NotesApp, setting: Setting) -> None:
    field_type: str = setting.field_type
    clue: str = ""
    value: str
    match field_type:
        case "bool":
            app.settings.set_value(setting.key, not app.settings.get_value(setting.key))
        case "int":
            min_value: int | None = setting.min_value
            max_value: int | None = setting.max_value
            if min_value is None and max_value is None:
                clue = "Enter any number"
            else:
                clue += "Range: "
                if min_value is not None:
                    clue += str(min_value)
                clue += ".."
                if max_value is not None:
                    clue += str(max_value)
            value = prompt_input(hint=clue, lowercase=False)
            if value == "%q":
                return
            elif value.isdigit() and "." not in value:
                edited: bool = app.settings.set_value(setting.key, int(value))
                if not edited:
                    clue = ""
                    if min_value is not None:
                        clue += str(min_value)
                    clue += ".."
                    if max_value is not None:
                        clue += str(max_value)
                    pause(f"number is not in range {clue}")

            else:
                pause("not a number")
        case "str":
            max_length: int | None = setting.max_length
            if max_length is not None:
                clue = f"Enter a text (max length is {max_length} characters)"
            else:
                clue = "Enter a text"
            value = prompt_input(hint=clue, lowercase=False)
            if value == "%q":
                return
            edited_str: bool = app.settings.set_value(setting.key, value)
            if not edited_str:
                pause(f"Text length is over than {max_length} characters")
        case "choice":
            result: str = ""
            choices = [choice for choice in setting.options]
            for i, choice in enumerate(choices):
                result += f"{i} {choice}\n"
            result += make_cyan("choose option ID")
            print(result)
            value = read_input(lowercase=False)
            if value == "%q":
                return
            elif (
                value.isdigit() and "." not in value and 0 <= int(value) < len(choices)
            ):
                app.settings.set_value(setting.key, choices[int(value)])
            else:
                pause("Wrong ID")


def get_header(text: str) -> str:
    width: int = shutil.get_terminal_size().columns
    if width <= 0:
        width = C.DEFAULT_TERMINAL_WIDTH
    padding: int = max(0, width - len(text) - 2)

    return (
        "=" * (padding // 2)
        + " "
        + make_cyan(text)
        + " "
        + "=" * (padding - padding // 2)
        + "\n"
    )


def display_main_menu(app: NotesApp) -> str:
    clear_screen()
    print(show_main_menu(app))
    mode: str = main_interface()
    return mode


def create_note_scenario(app: NotesApp) -> None:
    title: str = prompt_input(lowercase=False, hint="Note Name")
    while not title:
        title = prompt_input(
            hint="Title cannot be empty. Note Name", lowercase=False, danger=True
        )
    if title == C.KEY_SEARCH_QUIT:
        return
    text: str = prompt_input(hint="Text", lowercase=False)
    note: Note = app.create_note(title, text)
    open_note(app, note)


def search_scenario(app: NotesApp) -> None:
    query: str = prompt_input(
        hint=f"Enter a search query ({C.KEY_SEARCH_HELP} for help)"
    )
    while query == C.KEY_SEARCH_HELP:
        print(search_help())
        query = prompt_input(
            hint=f"Enter a search query ({C.KEY_SEARCH_HELP} for help)"
        )
    if query == C.KEY_SEARCH_QUIT:
        return
    results: list[Note] = app.search_note(query)
    if not results:
        pause("Nothing found")
    else:
        while True:
            clear_screen()
            print(
                get_header(
                    f"Search results: {len(results)} {'notes' if len(results) != 1 and len(results) != 0 else 'note'}"
                )
            )
            print(display_notes(get_visible_notes(results, True)))

            note_mode: str = prompt_input(
                hint=f"Enter ID to open, {C.KEY_QUIT} to go back"
            )
            if note_mode == C.KEY_QUIT:
                break
            if note_mode.isdigit() and "." not in note_mode:
                found_note: Note | None = app.get_note(int(note_mode))
                if found_note in results:
                    open_note(app, found_note)


def show_fatal_error() -> None:
    pause("An error occurred. Details in the app.log")


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
    if danger:
        print(make_red(hint))
    else:
        print(make_cyan(hint))
    return read_input(lowercase=lowercase, prompt_default_text=prompt_default_text)
