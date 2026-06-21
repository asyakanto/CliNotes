from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.notes import Note

from json import dump, load, JSONDecodeError
from pathlib import Path
import logging


class Storage:
    JSON_PATH: Path

    def __init__(self) -> None:
        self.JSON_PATH = Path(__file__).parent.parent / "notes.json"

    def load(self) -> list[dict]:
        try:
            with open(self.JSON_PATH, encoding="utf-8") as file:
                notes = load(file)
                logging.info(f"Loaded {len(notes)} notes")
                return notes
        except FileNotFoundError:
            logging.warning("Notes file not found, creating new")
            return []
        except JSONDecodeError:
            logging.error("JSON corrupted, starting fresh")
            return []

    def save(self, notes: list[Note]) -> None:
        from dataclasses import asdict

        lib = []
        for note in notes:
            lib.append(asdict(note))
        with open(self.JSON_PATH, "w", encoding="utf-8") as file:
            dump(lib, file, ensure_ascii=False, indent=2)
            logging.info(f"Saved {len(notes)} notes")
