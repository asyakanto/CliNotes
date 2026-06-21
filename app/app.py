from app.notes import Note
from app.storage import Storage

class NotesApp:
    def __init__(self):
        self.storage = Storage()
        self.notes = self.storage.load()
        self.notes = self._dictionary_to_object()
        self.notes = self._valid_notes_id()
        self.max_id = self._calculate_max_id()

    def _calculate_max_id(self):
        max_id = -1
        for note in self.notes:
            if note.id is not None and note.id > max_id:
                max_id = note.id
        return max_id

    def _valid_notes_id(self):
        self.max_id = int(self._calculate_max_id())
        ids = set()
        for note in self.notes:
            if note.id is None or note.id < 0 or note.id in ids or "." in str(note.id):
                self.max_id += 1
                note.id = self.max_id
            else:
                ids.add(note.id)
        self.storage.save(self.notes)
        return self.notes

    def _dictionary_to_object(self):
        lib = self.notes
        return [Note(**note) for note in lib]

    def create_note(self, title, text, tags):
        if not title.strip():
            return None
        self.max_id += 1
        note = Note(id=self.max_id, title=title, text=text, tags=tags)
        self.notes.append(note)
        self.storage.save(self.notes)
        return note

    def delete_note(self, id):
        for i, note in enumerate(self.notes):
            if id == note.id:
                self.notes.pop(i)
                self.storage.save(self.notes)
                return True
        return False
    
    def search_notes(self, search):
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