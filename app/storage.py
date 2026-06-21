from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.notes import Note

from json import dump, load, JSONDecodeError
from pathlib import Path


class Storage:
    JSON_PATH: Path

    def __init__(self) -> None:
        self.JSON_PATH = Path(__file__).parent.parent / "notes.json"

    def load(self) -> list[dict]:
        try:
            with open(self.JSON_PATH) as file:
                return load(file)
        except (FileNotFoundError, JSONDecodeError):
            return []

    def save(self, notes: list[Note]) -> None:
        from dataclasses import asdict

        lib = []
        for note in notes:
            lib.append(asdict(note))
        with open(self.JSON_PATH, "w") as file:
            dump(lib, file)
