from __future__ import annotations
from app.constants import RESET, RED, CYAN, DIM, SEPARATOR_WIDTH
from typing import TYPE_CHECKING
from os import name, system
from prompt_toolkit import prompt
from app.notes import get_tags


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


def display_notes(notes: list[Note], display_archieve=False) -> str:
    result = ""
    for note in notes:
        if not note.archieved:
            result += f"#{note.id} {note.title}" + "\n"
        elif display_archieve:
            result += make_muted(f"#{note.id} {note.title}") + "\n"
    return result


def show_note(app: NoteApp, note: Note) -> None:
    clear_screen()
    print(
        "=" * SEPARATOR_WIDTH
        + " "
        + make_cyan(note.title)
        + " "
        + "=" * SEPARATOR_WIDTH
    )
    if note.archieved:
        print(make_red("ARCHIEVED"))
    print(make_red(str(note.id)) + " #: " + make_muted(", ".join(note.tags)))
    print()
    print(note.text)
    print()


def interface(app: NoteApp, note: Note):
    if not note.archieved:
        while True:
            show_note(app, note)
            print(
                make_cyan("Choose action: q - quit; a - archieve note; e - edit note")
            )
            mode = input("> ").strip().lower()
            if mode == "q":
                break
            elif mode == "a":
                app.archieve_note(note)
                interface(app, note)
                break
            elif mode == "e":
                print(make_cyan("Edit: t - title, i - text"))
                mode = input("> ").strip().lower()
                if mode == "t":
                    new_title = prompt("New title: ", default=note.title).strip()
                    if new_title:
                        note.title = new_title
                if mode == "i":
                    new_text = prompt("New text: ", default=note.text).strip()
                    if new_text:
                        tags = get_tags(new_text)
                        tags.insert(0, note.tags[0])
                        note.tags = tags
                        note.text = new_text
                    else:
                        note.text = "-"
    else:
        while True:
            show_note(app, note)
            print(
                make_cyan("Choose action: q - quit; r - restore note; d - delete note")
            )
            mode = input("> ").strip().lower()
            if mode == "q":
                break
            elif mode == "r":
                note.archieved = False
                note.archieved_at = "0"
                interface(app, note)
                break
            elif mode == "d":
                app.delete_note(note)
                break
