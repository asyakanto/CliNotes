from app.notes import Note, get_date, get_tags
from app.storage import Storage
from app.constants import NO_NOTES_MAX_ID
import logging
from datetime import datetime


class NotesApp:
    notes: list[Note]
    max_id: int
    settings: dict
    storage: Storage

    def __init__(self) -> None:
        self.storage = Storage()

        self.notes = self.storage.load()
        self.notes = self._dictionary_to_object()

        self.max_id = self._calculate_max_id()

        self.notes = self._valid_notes_id()
        self.notes = self._delete_archived_notes()

        self.settings = self.storage.load_settings()

    def _dictionary_to_object(self) -> list[Note]:
        return [Note(**note) for note in self.notes]

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
            if (
                note.archived
                and (
                    current_date - datetime.strptime(note.archived_at, "%d-%m-%Y")
                ).days
                > 30
            ):
                to_delete.append(note)
        for note in to_delete:
            self.delete_note(note)
        return self.notes

    def create_note(
        self, title: str, text: str, tags: list[str], created: str
    ) -> Note | None:
        if not title.strip():
            return None
        if not text.strip():
            text = "-"
        self.max_id += 1
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
                note.text = "-"
                note.tags = [note.created]
        self.storage.save(self.notes)
        return note

    def restore_note(self, note: Note) -> Note:
        note.archived = False
        note.archived_at = "0"
        self.storage.save(self.notes)
        return note
