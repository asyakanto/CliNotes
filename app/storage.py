from __future__ import annotations
from json import dump, load, JSONDecodeError
from typing import TYPE_CHECKING, Any
from pathlib import Path
import logging
from app.constants import FILE_NOTES, FILE_SETTINGS
from dataclasses import asdict


if TYPE_CHECKING:
    from app.models import Note


class Storage:
    JSON_PATH: Path
    SETTINGS_PATH: Path

    def __init__(self) -> None:
        self.JSON_PATH = Path(__file__).parent.parent / FILE_NOTES
        self.SETTINGS_PATH = Path(__file__).parent.parent / FILE_SETTINGS

    def load(self) -> list[dict[str, Any]]:
        try:
            with open(self.JSON_PATH, encoding="utf-8") as file:
                notes: list[dict[str, Any]] = load(file)
                logging.info(f"Loaded {len(notes)} notes")
                return notes
        except FileNotFoundError:
            logging.warning("Notes file not found, creating new")
            return []
        except JSONDecodeError:
            logging.error("JSON corrupted, starting fresh")
            return []

    def save(self, notes: list[Note]) -> None:

        notes_serialized: list[dict[str, Any]] = [asdict(note) for note in notes]
        with open(self.JSON_PATH, "w", encoding="utf-8") as file:
            dump(notes_serialized, file, ensure_ascii=False, indent=2)
            logging.info(f"Saved {len(notes)} notes")

    def load_settings(self) -> dict[str, Any]:
        try:
            with open(self.SETTINGS_PATH, encoding="utf-8") as file:
                setting: dict[str, Any] = load(file)
                logging.info("Settings loaded")
                return setting
        except FileNotFoundError:
            logging.warning("Notes file not found, creating new")
            return {}
        except JSONDecodeError:
            logging.error("JSON corrupted, starting fresh")
            return {}

    def save_settings(self, settings: dict[str, Any]) -> None:
        with open(self.SETTINGS_PATH, "w", encoding="utf-8") as file:
            dump(settings, file, ensure_ascii=False, indent=2)
            logging.info("Settings updated")
