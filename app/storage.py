from __future__ import annotations

import logging
from dataclasses import asdict
from json import JSONDecodeError, dump, load
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from app.constants import Constants as C
from app.paths import data_dir
from app.settings import Settings

if TYPE_CHECKING:
    from app.models import Note, NoteDict

logger = logging.getLogger(__name__)


class Storage:
    NOTE_PATH: Path
    SETTINGS_PATH: Path
    TEMP_PATH: Path
    TEMP_SETTINGS: Path

    def __init__(self) -> None:
        self.root: Path = data_dir()
        self.root.mkdir(parents=True, exist_ok=True)
        self.NOTE_PATH = self.root / C.FILE_NOTES
        self.TEMP_PATH = self.root / C.FILE_TEMP
        self.SETTINGS_PATH = self.root / C.FILE_SETTINGS
        self.TEMP_SETTINGS = self.root / C.TEMP_SETTINGS_FILE

    def _atomic_write(
        self,
        temp_path: Path,
        final_path: Path,
        data: object,
        success_msg: str,
        error_msg: str,
    ) -> str:
        try:
            final_path.parent.mkdir(parents=True, exist_ok=True)
            with Path.open(temp_path, "w", encoding="utf-8") as file:
                dump(data, file, ensure_ascii=False, indent=2)
            Path.replace(temp_path, final_path)
            logger.info(success_msg)
        except OSError as e:
            logger.error(
                "Failed to replace file %s -> %s: %s", temp_path, final_path, e
            )
            return error_msg
        finally:
            try:
                if Path.exists(temp_path):
                    Path.unlink(temp_path)
                    logger.debug("Cleaned up temporary file: %s", temp_path)
            except OSError as e:
                logger.warning("Failed to delete temporary file %s: %s", temp_path, e)
        return ""

    def _is_expected_type(self, value: object, expected: type[object]) -> bool:
        return isinstance(value, expected)

    def _is_valid_tags(self, value: object) -> bool:
        return isinstance(value, list) and all(isinstance(tag, str) for tag in value)

    def _is_valid_note_id(self, value: object) -> bool:
        return isinstance(value, int) and not isinstance(value, bool)

    def _is_valid_note_raw(self, item: object) -> NoteDict | None:
        if not isinstance(item, dict):
            return None
        title: Any | None = item.get("title")
        text: Any | None = item.get("text")
        tags: Any | None = item.get("tags")
        created: Any | None = item.get("created")
        id: Any | None = item.get("id")
        archived: Any | None = item.get("archived")
        archived_at: Any | None = item.get("archived_at")

        if not (
            all(key in item for key in C.REQUIRED_KEYS)
            and self._is_expected_type(title, str)
            and self._is_expected_type(text, str)
            and self._is_valid_tags(tags)
            and self._is_valid_note_id(id)
            and self._is_expected_type(archived, bool)
            and self._is_expected_type(archived_at, str)
            and self._is_expected_type(created, str)
        ):
            return None

        result: NoteDict = {
            "title": cast("str", title),
            "text": cast("str", text),
            "tags": cast("list[str]", tags),
            "created": cast("str", created),
            "id": cast("int | None", id),
            "archived": cast("bool", archived),
            "archived_at": cast("str", archived_at),
        }

        return result

    def load(self) -> list[NoteDict]:
        try:
            with Path.open(self.NOTE_PATH, encoding="utf-8") as file:
                raw: Any = load(file)
        except FileNotFoundError:
            logger.warning("Notes file not found, creating new: %s", self.NOTE_PATH)
            return []
        except JSONDecodeError:
            logger.error("JSON corrupted, starting fresh")
            return []
        if not isinstance(raw, list):
            logger.error("Notes data is not a list")
            return []
        notes: list[NoteDict] = []
        for item in raw:
            result: NoteDict | None = self._is_valid_note_raw(item)
            if result is None:
                logger.warning("Skipping invalid note")
            else:
                notes.append(result)
        return notes

    def save(self, notes: list[Note]) -> str:
        notes_serialized: list[dict[str, Any]] = [asdict(note) for note in notes]
        success_msg: str = f"Saved {len(notes)} notes"
        failed_msg: str = f"Failed to save notes. Details in {C.FILE_LOG}"
        return self._atomic_write(
            self.TEMP_PATH, self.NOTE_PATH, notes_serialized, success_msg, failed_msg
        )

    def load_settings(self) -> Settings:
        try:
            with Path.open(self.SETTINGS_PATH, encoding="utf-8") as file:
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
        return self._atomic_write(
            self.TEMP_SETTINGS,
            self.SETTINGS_PATH,
            settings.settings_to_dict(),
            "Settings changed and saved successfully",
            f"Failed to save settings. Details in the {C.FILE_LOG}",
        )

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
