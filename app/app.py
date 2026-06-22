from app.notes import Note, get_date
from app.storage import Storage
from app.constants import NO_NOTES_MAX_ID
import logging
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
    ],
)


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
            else:
                ids.add(note.id)
        if duplicates_found:
            logging.warning(f"Fixed {duplicates_found} invalid ID")
            self.storage.save(self.notes)
        return self.notes

    def create_note(self, title: str, text: str, tags: list[str]) -> Note | None:
        if not title.strip():
            return None
        if not text.strip():
            text = "-"
        self.max_id += 1
        note = Note(id=self.max_id, title=title, text=text, tags=tags)
        self.notes.append(note)
        logging.info(f"Note created: #{note.id}: {note.title}")
        self.storage.save(self.notes)
        return note

    def get_note(self, id: int) -> Note | None:
        for note in self.notes:
            if id == note.id:
                return note
        return None

    def archieve_note(self, note: Note) -> None:
        note.archieved = True
        note.archieved_at = get_date(datetime.now())
        logging.info(f"Note archieved: #{note.id}: {note.title}")
        self.storage.save(self.notes)

    def delete_note(self, note: Note) -> None:
        id = note.id
        for i, note_item in enumerate(self.notes):
            if note_item.id == id:
                self.notes.pop(i)
        self.storage.save(self.notes)
