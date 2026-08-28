from __future__ import annotations

import logging
import os
from dataclasses import asdict
from json import JSONDecodeError, dump, load
from pathlib import Path
from typing import TYPE_CHECKING, Any

from app.constants import Constants as C
from app.settings import Settings

if TYPE_CHECKING:
    from app.models import Note, NoteDict

logger = logging.getLogger(__name__)


class Storage:
    NOTE_PATH: Path
    SETTINGS_PATH: Path
    TEMP_PATH: Path
    TEMP_SETTINGS: Path
    root: Path = Path(__file__).parent.parent

    def __init__(self) -> None:
        self.NOTE_PATH = Path(__file__).parent.parent / C.FILE_NOTES
        self.TEMP_PATH = Path(__file__).parent.parent / C.FILE_TEMP
        self.SETTINGS_PATH = Path(__file__).parent.parent / C.FILE_SETTINGS
        self.TEMP_SETTINGS = Path(__file__).parent.parent / C.TEMP_SETTINGS_FILE

    def load(self) -> list[NoteDict]:
        try:
            with open(self.NOTE_PATH, encoding="utf-8") as file:
                notes: list[NoteDict] = load(file)
                logger.info("Loaded %s notes", len(notes))
                return notes
        except FileNotFoundError:
            logger.warning("Notes file not found, creating new: %s", self.NOTE_PATH)
            return []
        except JSONDecodeError:
            logger.error("JSON corrupted, starting fresh")
            return []

    def save(self, notes: list[Note]) -> str:
        try:
            notes_serialized: list[dict[str, Any]] = [asdict(note) for note in notes]
            with open(self.TEMP_PATH, "w", encoding="utf-8") as file:
                dump(notes_serialized, file, ensure_ascii=False, indent=2)
            os.replace(self.TEMP_PATH, self.NOTE_PATH)
            logger.info("Saved %s notes", len(notes))
        except OSError as e:
            logger.error(
                "Failed to replace file %s -> %s: %s", self.TEMP_PATH, self.NOTE_PATH, e
            )
            return "Failed to save notes. Details in the app.log"
        finally:
            try:
                if os.path.exists(self.TEMP_PATH):
                    os.remove(self.TEMP_PATH)
                    logger.debug("Cleaned up temporary file: %s", self.TEMP_PATH)
            except OSError as e:
                logger.warning(
                    "Failed to delete temporary file %s: %s", self.TEMP_PATH, e
                )

        return ""

    def load_settings(self) -> Settings:
        try:
            with open(self.SETTINGS_PATH, encoding="utf-8") as file:
                setting_dict: dict[str, Any] = load(file)
                settings = Settings()
                settings.dict_to_settings(setting_dict)
                return settings
        except FileNotFoundError:
            logger.warning("Settings file not found: %s", self.SETTINGS_PATH)
            return Settings()
        except JSONDecodeError:
            logger.error("JSON corrupted, starting fresh")
            return Settings()

    def save_settings(self, settings: Settings) -> str:
        try:
            with open(self.TEMP_SETTINGS, "w", encoding="utf-8") as file:
                dump(settings.settings_to_dict(), file, ensure_ascii=False, indent=2)
            os.replace(self.TEMP_SETTINGS, self.SETTINGS_PATH)
            logger.info("Settings changed and saved successfully")
        except OSError as e:
            logger.error(
                "Failed to replace file %s -> %s: %s",
                self.TEMP_SETTINGS,
                self.SETTINGS_PATH,
                e,
            )
            return "Failed to save settings. Details in the app.log"
        finally:
            try:
                if os.path.exists(self.TEMP_SETTINGS):
                    os.remove(self.TEMP_SETTINGS)
                    logger.debug("Cleaned up temporary file: %s", self.TEMP_PATH)
            except OSError as e:
                logger.warning(
                    "Failed to delete temporary file %s: %s", self.TEMP_SETTINGS, e
                )

        return ""

    def update_notes_path(self, settings: Settings) -> bool:
        str_path: str = settings.get_str_value(C.SETTING_NOTES_PATH)
        path: Path = self.root / str_path
        if path.is_dir():
            self.NOTE_PATH = path / C.FILE_NOTES
            self.TEMP_PATH = path / C.FILE_TEMP
            return True

        self.NOTE_PATH = self.root / C.FILE_NOTES
        self.TEMP_PATH = self.root / C.FILE_TEMP
        return False
