from __future__ import annotations
from app.constants import RESET, RED, CYAN, DIM, SEPARATOR_WIDTH
from typing import TYPE_CHECKING
from os import name, system
from app.notes import get_date
from datetime import datetime, timedelta


if TYPE_CHECKING:
    from app.notes import Note
    from app.app import NoteApp


def clear_screen() -> None:
    if name == "nt":
        system("cls")
    else:
        system("clear")


def make_cyan(text: str) -> str:
    return CYAN + text + RESET


def make_muted(text: str) -> str:
    return DIM + text + RESET


def make_red(text: str) -> str:
    return RED + text + RESET


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
        "=" * SEPARATOR_WIDTH
        + " "
        + make_cyan(note.title)
        + " "
        + "=" * SEPARATOR_WIDTH
    )
    if note.archived:
        deleting_at = get_date(
            datetime.strptime(note.archived_at, "%d-%m-%Y") + timedelta(days=30)
        )
        print(make_red(f"ARCHIVED: note will be deleted at {deleting_at}"))
    print(make_red(str(note.id)) + " #: " + make_muted(", ".join(note.tags)))
    print()
    print(note.text)
    print()


def interface(app: NoteApp, note: Note) -> str:
    if not note.archived:
        show_note(note)
        print(make_cyan("Choose action: q - quit; a - archive note; e - edit note"))
        mode = input("> ").strip().lower()
        if mode == "q":
            return "quit"
        elif mode == "a":
            return "archive"
        elif mode == "e":
            print(make_cyan("Edit: t - title, i - text"))
            mode = input("> ").strip().lower()
            if mode == "t":
                return "change title"
            if mode == "i":
                return "change text"
        return "unknown"
    else:
        show_note(note)
        print(make_cyan("Choose action: q - quit; r - restore note; d - delete note"))
        mode = input("> ").strip().lower()
        if mode == "q":
            return "quit"
        elif mode == "r":
            return "restore"
        elif mode == "d":
            return "delete"
        return "unknown"
