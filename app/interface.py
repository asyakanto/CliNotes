from __future__ import annotations
from app.constants import (
    ANSI_RESET,
    ANSI_RED,
    ANSI_CYAN,
    ANSI_DIM,
    UI_SEPARATOR_WIDTH,
    UI_PROMPT,
    KEY_SETTINGS,
    KEY_TOGGLE_ARCHIVED,
    KEY_SEARCH,
    KEY_CREATE,
    KEY_QUIT,
    SETTING_SHOW_ARCHIVED,
    ACTION_DELETE,
    ACTION_RESTORE,
    ACTION_QUIT,
    KEY_DELETE,
    KEY_RESTORE,
    ACTION_UNKNOWN,
    ACTION_CHANGE_TEXT,
    ACTION_CHANGE_TITLE,
    KEY_EDIT_TEXT,
    KEY_EDIT_TITLE,
    KEY_EDIT,
    ACTION_ARCHIVE,
    KEY_ARCHIVE,
    AUTO_DELETE_DAYS,
    DATE_FORMAT,
)
from typing import TYPE_CHECKING
from os import name, system
from app.notes import get_date
from datetime import datetime, timedelta


if TYPE_CHECKING:
    from app.notes import Note
    from app.app import NotesApp


def clear_screen() -> None:
    if name == "nt":
        system("cls")
    else:
        system("clear")


def make_cyan(text: str) -> str:
    return ANSI_CYAN + text + ANSI_RESET


def make_muted(text: str) -> str:
    return ANSI_DIM + text + ANSI_RESET


def make_red(text: str) -> str:
    return ANSI_RED + text + ANSI_RESET


def display_notes(notes: list[Note], display_archive=False) -> str:
    result = ""
    for note in notes:
        if not note.archived:
            result += f"#{note.id} {note.title}" + "\n"
        elif display_archive:
            result += make_muted(f"#{note.id} {note.title}") + "\n"
    return result


def show_note(note: Note) -> None:
    clear_screen()
    print(
        "=" * UI_SEPARATOR_WIDTH
        + " "
        + make_cyan(note.title)
        + " "
        + "=" * UI_SEPARATOR_WIDTH
    )
    if note.archived:
        try:
            deleting_at = get_date(
                datetime.strptime(note.archived_at, DATE_FORMAT)
                + timedelta(days=AUTO_DELETE_DAYS)
            )
        except ValueError:
            deleting_at = "unknown date"
        print(make_red(f"ARCHIVED: note will be deleted at {deleting_at}"))
    print(make_red(str(note.id)) + " #: " + make_muted(", ".join(note.tags)))
    print()
    print(note.text)
    print()


def interface(note: Note) -> str:
    if not note.archived:
        show_note(note)
        print(
            make_cyan(
                f"Choose action: {KEY_QUIT} - quit; {KEY_ARCHIVE} - archive note; {KEY_EDIT} - edit note"
            )
        )
        mode = input(UI_PROMPT).strip().lower()
        if mode == KEY_QUIT:
            return ACTION_QUIT
        elif mode == KEY_ARCHIVE:
            return ACTION_ARCHIVE
        elif mode == KEY_EDIT:
            print(make_cyan(f"Edit: {KEY_EDIT_TITLE} - title, {KEY_EDIT_TEXT} - text"))
            mode = input(UI_PROMPT).strip().lower()
            if mode == KEY_EDIT_TITLE:
                return ACTION_CHANGE_TITLE
            if mode == KEY_EDIT_TEXT:
                return ACTION_CHANGE_TEXT
        return ACTION_UNKNOWN
    else:
        show_note(note)
        print(
            make_cyan(
                f"Choose action: {KEY_QUIT} - quit; {KEY_RESTORE} - restore note; {KEY_DELETE} - delete note"
            )
        )
        mode = input(UI_PROMPT).strip().lower()
        if mode == KEY_QUIT:
            return ACTION_QUIT
        elif mode == KEY_RESTORE:
            return ACTION_RESTORE
        elif mode == KEY_DELETE:
            return ACTION_DELETE
        return ACTION_UNKNOWN


def show_main_menu(app: NotesApp) -> str:
    clear_screen()
    print(make_red("CliNotes") + ": " + get_date(datetime.now()))
    print()

    print(display_notes(app.notes, app.settings.get(SETTING_SHOW_ARCHIVED)))

    print()

    print(
        make_cyan(
            "Actions: {ID}"
            + f"- open note; {KEY_QUIT} - quit; {KEY_CREATE} - create; {KEY_SEARCH} - search; {KEY_TOGGLE_ARCHIVED} - show archived; {KEY_SETTINGS} - settings"
        )
    )
    mode = input(UI_PROMPT).strip().lower()

    return mode
