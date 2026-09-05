"""Business logic of the CliNotes application."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING

from app.constants import Constants
from app.models import Note, get_date, get_local_now, get_plural, get_tags
from app.search import apply_filters, parse_query
from app.storage import Storage

if TYPE_CHECKING:
    from app.settings import Settings

logger = logging.getLogger(__name__)


class NotesApp:
    """Central application logic: notes, tags, settings and saving."""

    notes: list[Note]
    max_id: int
    settings: Settings
    storage: Storage

    # ── Life cycle ───────────────────────────
    def __init__(self) -> None:
        """Initialize storage, load settings and notes."""
        self._notifications: list[str] = []
        self.storage = Storage()
        self.settings = self.storage.load_settings()
        self.apply_notes_path()

    def _load_notes(self) -> None:
        self.notes = [Note(**n) for n in self.storage.load()]

        self.max_id = self._calculate_max_id()

        self.notes = self._fix_invalid_ids()
        self.notes = self._delete_archived_notes()
        self.sync_tags_if_enabled()

    def _calculate_max_id(self) -> int:
        max_id: int = Constants.NO_NOTES_MAX_ID
        for note in self.notes:
            if (
                note.id is not None
                and not isinstance(note.id, bool)
                and not isinstance(note.id, str)
                and note.id > max_id
                and isinstance(note.id, int)
            ):
                max_id = note.id
        return max_id

    def _fix_invalid_ids(self) -> list[Note]:
        ids: set[int] = set()
        duplicates_found: int = 0
        for note in self.notes:
            if note.id is None or note.id < 0 or note.id in ids:
                self.max_id += 1
                note.id = self.max_id
                duplicates_found += 1
            ids.add(note.id)
        if duplicates_found:
            duplicate_message: str = (
                f"Fixed {get_plural(duplicates_found, 'invalid ID')}"
            )
            self.add_notification(duplicate_message)
            logger.warning(duplicate_message)
            self._save_if_auto()
        return self.notes

    def _delete_archived_notes(self) -> list[Note]:
        current_date: datetime = get_local_now()
        to_delete: list[Note] = []
        notes_before_deleting: int = len(self.notes)
        for note in self.notes:
            if note.archived_at != Constants.DEFAULT_ARCHIVED_AT and note.archived:
                try:
                    if (
                        current_date
                        - datetime.strptime(
                            note.archived_at,
                            Constants.DATE_FORMAT_STORAGE,
                        ).replace(tzinfo=get_local_now().tzinfo)
                    ).days > self.settings.get_int_value(
                        Constants.SETTING_AUTO_DELETE_DAYS
                    ):
                        to_delete.append(note)
                except ValueError:
                    continue
        for note in to_delete:
            self.delete_note(note)
        notes_after_deleting: int = len(self.notes)
        if notes_after_deleting != notes_before_deleting:
            deleted: int = notes_before_deleting - notes_after_deleting
            self.add_notification(f"Deleted {get_plural(deleted, 'expired note')}")
        return self.notes

    # ── CRUD ─────────────────────────────────

    def create_note(self, title: str, text: str) -> Note:
        """Create a note, auto-assign ID and build tags."""
        self.max_id += 1
        created: str = get_date(get_local_now(), Constants.DATE_FORMAT_STORAGE)
        note: Note = Note(
            id=self.max_id,
            title=title,
            text=text,
            tags=self._build_tags(text, created),
            created=created,
        )
        self.notes.append(note)
        logger.info("Note created: #%s: %s", note.id, note.title)
        self._save_if_auto()
        return note

    def get_note(self, idd: int) -> Note | None:
        """Return the note with the given ID, or None."""
        for note in self.notes:
            if idd == note.id:
                return note
        return None

    def edit_note(self, note: Note, new_title: str, new_text: str) -> Note:
        """Update title/text and rebuild tags of a note."""
        if new_title and new_title != note.title:
            note.title = new_title
        if new_text != note.text:
            note.tags = self._build_tags(new_text, note.created)
            note.text = new_text
        self._save_if_auto()
        return note

    def archive_note(self, note: Note) -> Note:
        """Mark a note as archived."""
        note.archived = True
        note.archived_at = get_date(get_local_now(), Constants.DATE_FORMAT_STORAGE)
        logger.info("Note archived: #%s: %s", note.id, note.title)
        self._save_if_auto()
        return note

    def restore_note(self, note: Note) -> Note:
        """Restore an archived note."""
        note.archived = False
        note.archived_at = Constants.DEFAULT_ARCHIVED_AT
        self._save_if_auto()
        return note

    def delete_note(self, note: Note) -> None:
        """Remove a note from the list."""
        note_id: int | None = note.id
        for i, note_item in enumerate(self.notes):
            if note_item.id == note_id:
                self.notes.pop(i)
                break
        self._save_if_auto()

    # ── Search ───────────────────────────────

    def search_note(self, query: str) -> list[Note]:
        """Return notes matching the parsed query filters."""
        filters: list[tuple[str, str]] = parse_query(
            query, self.settings.active_tag_prefixes()
        )
        results: list[Note] = apply_filters(self.notes, filters)
        return results

    # ── Tags ─────────────────────────────────

    def _sync_tags_with_settings(self) -> list[Note]:
        counter: int = 0
        for note in self.notes:
            new_tags = self._build_tags(note.text, note.created)
            if new_tags != note.tags:
                note.tags = new_tags
                counter += 1

        if counter > 0:
            self.add_notification(f"Updated {get_plural(counter, 'note')} tags")
            self._save_if_auto()
        return self.notes

    def sync_tags_if_enabled(self) -> None:
        """Sync tags from text if the setting is enabled."""
        if self.settings.get_bool_value(Constants.SETTING_AUTO_SYNC_TAGS):
            self._sync_tags_with_settings()

    def _build_tags(self, text: str, created: str) -> list[str]:
        tags: list[str] = get_tags(text, self.settings.active_tag_prefixes())
        if self.settings.get_bool_value(Constants.SETTING_AUTO_DATE_TAG):
            tags.insert(0, created)
        return tags

    # ── Settings ─────────────────────────────
    def save_settings(self) -> None:
        """Persist settings to disk."""
        result: str = self.storage.save_settings(self.settings)
        if result:
            self.add_notification(result)

    def reset_settings(self) -> None:
        """Reset all settings to defaults and save."""
        self.settings.reset_all()
        self.save_settings()

    def apply_notes_path(self) -> None:
        """Apply the configured notes path and load notes."""
        result: bool = self.storage.update_notes_path(self.settings)
        if not result:
            self.settings.reset_setting(Constants.SETTING_NOTES_PATH)
            self.save_settings()
            self.add_notification("Invalid path, using default")

        self._load_notes()

    def apply_log_level(self) -> None:
        """Apply the configured logging level."""
        level: str = self.settings.get_str_value(Constants.SETTING_LOG_LEVEL)
        logger: logging.Logger = logging.getLogger()
        logger_level: int | None = Constants.LOG_LEVEL_MAP.get(level)
        if logger_level is not None:
            logger.setLevel(logger_level)
        else:
            logger.warning("Unknown logging level: %s", level)

    def toggle_show_archived(self) -> None:
        """Flip the show-archived setting."""
        self.settings.set_value(
            Constants.SETTING_SHOW_ARCHIVED,
            not self.settings.get_bool_value(Constants.SETTING_SHOW_ARCHIVED),
        )
        self.save_settings()

    # ── Saving ───────────────────────────────
    def save_notes(self) -> None:
        """Persist notes to disk."""
        result: str = self.storage.save(self.notes)
        if result:
            self.add_notification(result)

    def _save_if_auto(self) -> None:
        if self.settings.get_bool_value(Constants.SETTING_AUTO_SAVE):
            self.save_notes()

    # ── Notifications ────────────────────────

    def add_notification(self, message: str) -> None:
        """Queue a notification message."""
        if message.strip():
            self._notifications.append(message.strip())

    def pop_notifications(self) -> list[str]:
        """Return all queued notifications and clear them."""
        notifications: list[str] = self._notifications
        self._notifications = []
        return notifications
