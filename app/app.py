from app.notes import Note, get_date, get_tags
from app.storage import Storage
from app.constants import (
    NO_NOTES_MAX_ID,
    DEFAULT_ARCHIVED_AT,
    DEFAULT_TEXT,
    DATE_FORMAT,
    AUTO_DELETE_DAYS,
)
import logging
from datetime import datetime


class NotesApp:
    notes: list[Note]
    max_id: int
    settings: dict
    storage: Storage

    def __init__(self) -> None:
        self.storage = Storage()

        raw_notes = self.storage.load()
        self.notes = [Note(**n) for n in raw_notes]

        self.max_id = self._calculate_max_id()

        self.notes = self._valid_notes_id()
        self.notes = self._delete_archived_notes()

        self.settings = self.storage.load_settings()

    def _calculate_max_id(self) -> int:
        max_id = NO_NOTES_MAX_ID
        for note in self.notes:
            if note.id is not None and note.id > max_id and "." not in str(note.id):
                max_id = note.id
        return max_id

    def _valid_notes_id(self) -> list[Note]:
        ids = set()
        duplicates_found = 0
        for note in self.notes:
            if note.id is None or note.id < 0 or note.id in ids or "." in str(note.id):
                self.max_id += 1
                note.id = self.max_id
                duplicates_found += 1
            ids.add(note.id)
        if duplicates_found:
            logging.warning(f"Fixed {duplicates_found} invalid ID")
            self.storage.save(self.notes)
        return self.notes

    def _delete_archived_notes(self) -> list[Note]:
        current_date = datetime.now()
        to_delete = []
        for note in self.notes:
            if note.archived_at != DEFAULT_ARCHIVED_AT and note.archived:
                try:
                    if (
                        current_date - datetime.strptime(note.archived_at, DATE_FORMAT)
                    ).days > AUTO_DELETE_DAYS:
                        to_delete.append(note)
                except ValueError:
                    continue
        for note in to_delete:
            self.delete_note(note)
        return self.notes

    def create_note(self, title: str, text: str) -> Note:
        if not text.strip():
            text = DEFAULT_TEXT
        self.max_id += 1
        tags = get_tags(text)
        created = get_date(datetime.now())
        tags.insert(0, created)
        note = Note(id=self.max_id, title=title, text=text, tags=tags, created=created)
        self.notes.append(note)
        logging.info(f"Note created: #{note.id}: {note.title}")
        self.storage.save(self.notes)
        return note

    def get_note(self, id: int) -> Note | None:
        for note in self.notes:
            if id == note.id:
                return note
        return None

    def archive_note(self, note: Note) -> Note:
        note.archived = True
        note.archived_at = get_date(datetime.now())
        logging.info(f"Note archived: #{note.id}: {note.title}")
        self.storage.save(self.notes)
        return note

    def delete_note(self, note: Note) -> None:
        id = note.id
        for i, note_item in enumerate(self.notes):
            if note_item.id == id:
                self.notes.pop(i)
        self.storage.save(self.notes)
        return None

    def edit_note(self, note: Note, new_title: str, new_text: str) -> Note:
        if new_title and new_title != note.title:
            note.title = new_title
        if new_text != note.text:
            if new_text:
                tags = get_tags(new_text)
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
