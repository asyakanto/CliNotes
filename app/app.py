from app.notes import Note
from app.storage import Storage
from app.constants import NO_NOTES_MAX_ID
import logging


class NotesApp:
    notes: list[Note]
    max_id: int

    def __init__(self) -> None:
        self.storage = Storage()
        self.notes = self.storage.load()
        self.notes = self._dictionary_to_object()
        self.notes = self._valid_notes_id()
        self.max_id = self._calculate_max_id()

    def _calculate_max_id(self) -> int:
        max_id = NO_NOTES_MAX_ID
        for note in self.notes:
            if note.id is not None and note.id > max_id:
                max_id = note.id
        return max_id

    def _valid_notes_id(self) -> list[Note]:
        self.max_id = int(self._calculate_max_id())
        ids = set()
        duplicates_found = 0
        for note in self.notes:
            if note.id is None or note.id < 0 or note.id in ids or "." in str(note.id):
                self.max_id += 1
                note.id = self.max_id
                duplicates_found += 1
            else:
                ids.add(note.id)
        if duplicates_found:
            logging.warning(f"Fixed {duplicates_found} invalid ID")
            self.storage.save(self.notes)
        return self.notes

    def _dictionary_to_object(self) -> list[Note]:
        lib = self.notes
        return [Note(**note) for note in lib]

    def create_note(self, title: str, text: str, tags: list[str]) -> Note | None:
        if not title.strip():
            return None
        self.max_id += 1
        note = Note(id=self.max_id, title=title, text=text, tags=tags)
        self.notes.append(note)
        logging.info(f"Note created: #{note.id}: {note.title}")
        self.storage.save(self.notes)
        return note

    def delete_note(self, id: int) -> bool:
        for i, note in enumerate(self.notes):
            if id == note.id:
                self.notes.pop(i)
                logging.info(f"Note deleted: #{note.id}: {note.title}")
                self.storage.save(self.notes)
                return True
        return False

    def search_notes(self, search: str) -> list[Note]:
        if not search:
            return self.notes
        search = search.lower()
        found_notes = []
        search_by = "title"
        if search[0] == "@":
            search = search[1:]
            search_by = "tags"
        if search_by == "title":
            for note in self.notes:
                if search in note.title.lower():
                    found_notes.append(note)
        elif search_by == "tags":
            for note in self.notes:
                for tag in note.tags:
                    if search in tag:
                        found_notes.append(note)
                        break
        return found_notes

    def get_note(self, id: int) -> Note | None:
        for note in self.notes:
            if id == note.id:
                return note
        return None

    def edit_note(self, id: int, title: str, text: str, tags: list[str]) -> Note | None:
        note = self.get_note(id)
        if note is None:
            logging.warning("Editing a non-existent note")
            return None
        if title.strip():
            note.title = title.strip()
        if text.strip():
            note.text = text.strip()
        if tags:
            note.tags = tags
        self.storage.save(self.notes)
        logging.info(f"Note edited: #{note.id}: {note.title}")
        return note
