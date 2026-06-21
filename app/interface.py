from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.notes import Note

from os import name, system
from app.constants import RED, GREEN, YELLOW, CYAN, DIM, RESET, SEPARATOR_WIDTH


def clear_screen() -> None:
    if name == "nt":
        system("cls")
    else:
        system("clear")


def display_notes(notes: list[Note]) -> str:
    result = ""
    for note in notes:
        result += f"#{note.id} {note.title}" + "\n"
        result += (note.text if note.text else "-") + "\n"
        tags_str = ", ".join(note.tags)
        result += "@: " + mk_muted(tags_str) + "\n" if note.tags else ""
        result += f"{'=' * SEPARATOR_WIDTH}" + "\n\n"
    return result


def display_notes_names(notes: list[Note]) -> str:
    result = ""
    for note in notes:
        result += f"#{note.id} {note.title}" + "\n"
    return result


def mk_error(text: str) -> str:
    return RED + text + RESET


def mk_success(text: str) -> str:
    return GREEN + text + RESET


def mk_warning(text: str) -> str:
    return YELLOW + text + RESET


def mk_prompt(text: str) -> str:
    return CYAN + text + RESET


def mk_muted(text: str) -> str:
    return DIM + text + RESET
