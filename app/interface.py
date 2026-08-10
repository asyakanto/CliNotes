from __future__ import annotations

from datetime import datetime, timedelta
from os import name, system
from typing import TYPE_CHECKING

from prompt_toolkit import prompt

from app.constants import (
    ACTION_ARCHIVE,
    ACTION_CHANGE_TEXT,
    ACTION_CHANGE_TITLE,
    ACTION_DELETE,
    ACTION_QUIT,
    ACTION_RESTORE,
    ACTION_TYPE,
    ACTION_UNKNOWN,
    ANSI_CYAN,
    ANSI_DIM,
    ANSI_RED,
    ANSI_RESET,
    AUTO_DELETE_DAYS,
    DATE_FORMAT_STORAGE,
    KEY_ARCHIVE,
    KEY_CREATE,
    KEY_DELETE,
    KEY_EDIT,
    KEY_EDIT_TEXT,
    KEY_EDIT_TITLE,
    KEY_QUIT,
    KEY_RESTORE,
    KEY_SEARCH,
    KEY_SETTINGS,
    KEY_TOGGLE_ARCHIVED,
    SEPARATOR_WIDTH,
    SETTING_SHOW_ARCHIVED,
    UI_PROMPT,
)
from app.models import get_date, get_local_now

if TYPE_CHECKING:
    from app.app import NotesApp
    from app.models import Note


def clear_screen() -> None:
    if name == "nt":
        system("cls")
    else:
        system("clear")


def open_note(app: NotesApp, note: Note) -> None:
    while True:
        clear_screen()
        print(show_note(note, app))
        action: ACTION_TYPE = note_interface(note)

        if action == ACTION_QUIT:
            break
        elif action == ACTION_ARCHIVE:
            app.archive_note(note)
        elif action == ACTION_CHANGE_TITLE:
            new_title: str = prompt("New title: ", default=note.title).strip()
            app.edit_note(note, new_title, note.text)
        elif action == ACTION_CHANGE_TEXT:
            new_text: str = prompt("New text: ", default=note.text).strip()
            app.edit_note(note, note.title, new_text)
        elif action == ACTION_UNKNOWN:
            print()
            input(make_red("Wrong action"))
        elif action == ACTION_RESTORE:
            app.restore_note(note)
        elif action == ACTION_DELETE:
            confirm: str = input(make_red("Delete this note? (y/n): ")).strip().lower()
            if confirm == "y":
                app.delete_note(note)
                break


def make_cyan(text: str) -> str:
    return ANSI_CYAN + text + ANSI_RESET


def make_muted(text: str) -> str:
    return ANSI_DIM + text + ANSI_RESET


def make_red(text: str) -> str:
    return ANSI_RED + text + ANSI_RESET


def display_notes(notes: list[Note], display_archive: bool = False) -> str:
    lines: list[str] = []
    for note in notes:
        if not note.archived:
            lines.append(f"#{note.id} {note.title}")
        elif display_archive:
            lines.append(make_muted(f"#{note.id} {note.title}"))
    return "\n".join(lines) + "\n"


def show_note(note: Note, app: NotesApp) -> str:
    result: str = ""
    value: int | None | bool | str = app.settings.get_value(SEPARATOR_WIDTH)
    if isinstance(value, int):
        separator: str = "=" * int(value)
    result += separator + " " + make_cyan(note.title) + " " + separator + "\n"
    if note.archived:
        deleting_at: str
        try:
            deleting_at = get_date(
                datetime.strptime(
                    note.archived_at,
                    DATE_FORMAT_STORAGE,
                ).replace(tzinfo=get_local_now().tzinfo)
                + timedelta(days=AUTO_DELETE_DAYS),
                app.settings.date_pattern(),
            )
        except ValueError:
            deleting_at = "unknown date"
        result += make_red(f"ARCHIVED: note will be deleted at {deleting_at}" + "\n")
    result += make_red(str(note.id)) + " #: " + make_muted(", ".join(note.tags)) + "\n"
    result += "\n"
    result += note.text + "\n"
    result += "\n"
    if not note.archived:
        result += make_cyan(
            f"Choose action: {KEY_QUIT} - quit; {KEY_ARCHIVE} - archive note; {KEY_EDIT} - edit note"
            + "\n"
        )
    else:
        result += make_cyan(
            f"Choose action: {KEY_QUIT} - quit; {KEY_RESTORE} - restore note; {KEY_DELETE} - delete note"
            + "\n"
        )
    return result


def note_interface(note: Note) -> ACTION_TYPE:
    mode: str
    if not note.archived:
        mode = input(UI_PROMPT).strip().lower()
        if mode == KEY_QUIT:
            return ACTION_QUIT
        elif mode == KEY_ARCHIVE:
            return ACTION_ARCHIVE
        elif mode == KEY_EDIT:
            editing_mode: str = (
                input(
                    make_cyan(f"Edit: {KEY_EDIT_TITLE} - title, {KEY_EDIT_TEXT} - text")
                    + "\n"
                    + UI_PROMPT
                )
                .strip()
                .lower()
            )
            if editing_mode == KEY_EDIT_TITLE:
                return ACTION_CHANGE_TITLE
            if editing_mode == KEY_EDIT_TEXT:
                return ACTION_CHANGE_TEXT
        return ACTION_UNKNOWN
    else:
        mode = input(UI_PROMPT).strip().lower()
        if mode == KEY_QUIT:
            return ACTION_QUIT
        elif mode == KEY_RESTORE:
            return ACTION_RESTORE
        elif mode == KEY_DELETE:
            return ACTION_DELETE
        return ACTION_UNKNOWN


def show_main_menu(app: NotesApp) -> str:
    result: str = ""
    result += (
        make_red("CliNotes")
        + ": "
        + get_date(
            get_local_now(),
            app.settings.date_pattern(),
        )
        + "\n"
    )
    result += "\n"
    result += get_notifications(app)

    result += (
        display_notes(app.notes, bool(app.settings.get_value(SETTING_SHOW_ARCHIVED)))
        + "\n"
    )

    result += make_cyan(
        "Actions: {ID}"
        + f" - open note; {KEY_QUIT} - quit; {KEY_CREATE} - create; {KEY_SEARCH} - search; {KEY_TOGGLE_ARCHIVED} - show archived; {KEY_SETTINGS} - settings"
        + "\n"
    )

    return result


def main_interface(_app: NotesApp) -> str:

    mode = input(UI_PROMPT).strip().lower()

    return mode


def get_notifications(app: NotesApp) -> str:
    if not app._notifications:
        return ""

    result: str = ""

    for notification in app.pop_notifications():
        result += make_red("[!] " + notification + "\n")
    return result + "\n"
