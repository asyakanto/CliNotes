from __future__ import annotations

import logging
from dataclasses import asdict
from json import JSONDecodeError, dump, load
from pathlib import Path
from typing import TYPE_CHECKING, Any

from app.constants import FILE_NOTES, FILE_SETTINGS
from app.settings import Settings

if TYPE_CHECKING:
    from app.models import Note

logger = logging.getLogger(__name__)


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
                logger.info(f"Loaded {len(notes)} notes")
                return notes
        except FileNotFoundError:
            logger.warning("Notes file not found, creating new")
            return []
        except JSONDecodeError:
            logger.error("JSON corrupted, starting fresh")
            return []

    def save(self, notes: list[Note]) -> None:

        notes_serialized: list[dict[str, Any]] = [asdict(note) for note in notes]
        with open(self.JSON_PATH, "w", encoding="utf-8") as file:
            dump(notes_serialized, file, ensure_ascii=False, indent=2)
            logger.info(f"Saved {len(notes)} notes")

    def load_settings(self) -> Settings:
        try:
            with open(self.SETTINGS_PATH, encoding="utf-8") as file:
                setting_dict: dict[str, Any] = load(file)
                settings = Settings()
                settings.dict_to_settings(setting_dict)
                return settings
        except FileNotFoundError:
            logger.warning("Notes file not found, creating new")
            return Settings()
        except JSONDecodeError:
            logger.error("JSON corrupted, starting fresh")
            return Settings()

    def save_settings(self, settings: Settings) -> None:
        with open(self.SETTINGS_PATH, "w", encoding="utf-8") as file:
            dump(settings.settings_to_dict(), file, ensure_ascii=False, indent=2)
            logger.info("Settings updated")
