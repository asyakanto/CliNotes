import logging
from datetime import datetime

from app.constants import (
    AUTO_DELETE_DAYS,
    DATE_FORMAT_STORAGE,
    DEFAULT_ARCHIVED_AT,
    DEFAULT_TEXT,
    NO_NOTES_MAX_ID,
)
from app.models import Note, get_date, get_local_now, get_tags
from app.search import apply_filters, parse_query
from app.settings import Settings
from app.storage import Storage

logger = logging.getLogger(__name__)


class NotesApp:
    notes: list[Note]
    max_id: int
    settings: Settings
    storage: Storage

    def __init__(self) -> None:
        self.storage = Storage()
        self.settings = self.storage.load_settings()

        raw_notes = self.storage.load()
        self.notes = [Note(**n) for n in raw_notes]

        self.max_id = self._calculate_max_id()

        self._notifications: list[str] = []
        self.notes = self._fix_invalid_ids()
        self.notes = self._delete_archived_notes()

    def _calculate_max_id(self) -> int:
        max_id: int = NO_NOTES_MAX_ID
        for note in self.notes:
            if note.id is not None and note.id > max_id and "." not in str(note.id):
                max_id = note.id
        return max_id

    def _fix_invalid_ids(self) -> list[Note]:
        ids: set[int] = set()
        duplicates_found: int = 0
        for note in self.notes:
            if note.id is None or note.id < 0 or note.id in ids or "." in str(note.id):
                self.max_id += 1
                note.id = self.max_id
                duplicates_found += 1
            ids.add(note.id)
        if duplicates_found:
            logger.warning(f"Fixed {duplicates_found} invalid ID")
            self.storage.save(self.notes)
        return self.notes

    def _delete_archived_notes(self) -> list[Note]:
        current_date: datetime = get_local_now()
        to_delete: list[Note] = []
        notes_before_deleting: int = len(self.notes)
        for note in self.notes:
            if note.archived_at != DEFAULT_ARCHIVED_AT and note.archived:
                try:
                    if (
                        current_date
                        - datetime.strptime(
                            note.archived_at,
                            DATE_FORMAT_STORAGE,
                        ).replace(tzinfo=get_local_now().tzinfo)
                    ).days > AUTO_DELETE_DAYS:
                        to_delete.append(note)
                except ValueError:
                    continue
        for note in to_delete:
            self.delete_note(note)
        notes_after_deleting: int = len(self.notes)
        if notes_after_deleting != notes_before_deleting:
            self.add_notification(
                f"Deleted {notes_before_deleting - notes_after_deleting} expired notes"
            )
        return self.notes

    def create_note(self, title: str, text: str) -> Note:
        if not text.strip():
            text = DEFAULT_TEXT
        self.max_id += 1
        tags: list[str] = get_tags(text)
        created: str = get_date(get_local_now(), DATE_FORMAT_STORAGE)
        tags.insert(0, created)
        note: Note = Note(
            id=self.max_id, title=title, text=text, tags=tags, created=created
        )
        self.notes.append(note)
        logger.info(f"Note created: #{note.id}: {note.title}")
        self.storage.save(self.notes)
        return note

    def get_note(self, id: int) -> Note | None:
        for note in self.notes:
            if id == note.id:
                return note
        return None

    def archive_note(self, note: Note) -> Note:
        note.archived = True
        note.archived_at = get_date(get_local_now(), DATE_FORMAT_STORAGE)
        logger.info(f"Note archived: #{note.id}: {note.title}")
        self.storage.save(self.notes)
        return note

    def delete_note(self, note: Note) -> None:
        note_id: int | None = note.id
        for i, note_item in enumerate(self.notes):
            if note_item.id == note_id:
                self.notes.pop(i)
                break
        self.storage.save(self.notes)

    def edit_note(self, note: Note, new_title: str, new_text: str) -> Note:
        if new_title and new_title != note.title:
            note.title = new_title
        if new_text != note.text:
            if new_text:
                tags: list[str] = get_tags(new_text)
                tags.insert(0, note.created)
                note.tags = tags
                note.text = new_text
            else:
                note.text = DEFAULT_TEXT
                note.tags = [note.created]
        self.storage.save(self.notes)
        return note

    def restore_note(self, note: Note) -> Note:
        note.archived = False
        note.archived_at = DEFAULT_ARCHIVED_AT
        self.storage.save(self.notes)
        return note

    def search_note(self, query: str) -> list[Note]:
        filters: list[tuple[str, str]] = parse_query(query)
        results: list[Note] = apply_filters(self.notes, filters)
        return results

    def add_notification(self, message: str) -> None:
        if message.strip():
            self._notifications.append(message.strip())

    def pop_notifications(self) -> list[str]:
        notifications: list[str] = self._notifications
        self._notifications = []
        return notifications
