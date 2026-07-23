from app.notes import Note, get_date, get_tags
from app.storage import Storage
from app.constants import (
    NO_NOTES_MAX_ID,
    DEFAULT_ARCHIVED_AT,
    DEFAULT_TEXT,
    DATE_FORMAT,
    AUTO_DELETE_DAYS,
    TAG_PREFIXES,
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
        max_id: int = NO_NOTES_MAX_ID
        for note in self.notes:
            if note.id is not None and note.id > max_id and "." not in str(note.id):
                max_id = note.id
        return max_id

    def _valid_notes_id(self) -> list[Note]:
        ids: set[int] = set()
        duplicates_found: int = 0
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
        current_date: datetime = datetime.now()
        to_delete: list[Note] = []
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
        tags: list[str] = get_tags(text)
        created: str = get_date(datetime.now())
        tags.insert(0, created)
        note: Note = Note(
            id=self.max_id, title=title, text=text, tags=tags, created=created
        )
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
        note_id: int | None = note.id
        for i, note_item in enumerate(self.notes):
            if note_item.id == note_id:
                self.notes.pop(i)
        self.storage.save(self.notes)
        return None

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

    @staticmethod
    def _split_with_quotes(query: str) -> list[str]:
        tokens: list[str] = []
        current_token: str = ""
        in_quotes: bool = False
        for char in query:
            if char == '"':
                in_quotes = not in_quotes
            elif char == " " and not in_quotes:
                if current_token:
                    tokens.append(current_token.strip().lower())
                    current_token = ""
            else:
                current_token += char
        if current_token:
            tokens.append(current_token.strip().lower())
        return tokens

    @staticmethod
    def _merge_prefixes(tokens: list[str]) -> list[str]:
        current_token: str = ""
        merged_tokens: list[str] = []
        for token in tokens:
            if token.startswith("title:") or token.startswith("text:"):
                if current_token:
                    merged_tokens.append(current_token)
                current_token = token
            else:
                merged_tokens.append(current_token + token)
                current_token = ""
        if current_token:
            merged_tokens.append(current_token)
        return merged_tokens

    def search_note(self, query: str) -> list[Note]:
        raw_parts: list[str] = self._split_with_quotes(query)
        raw_parts = self._merge_prefixes(raw_parts)
        filters: list[tuple[str, str]] = []

        for part in raw_parts:
            is_tag: bool = False
            for sep in TAG_PREFIXES:
                if part.strip().startswith(sep):
                    filters.append(("tag", part.removeprefix(sep).strip()))
                    is_tag = True
                    break
            if is_tag:
                continue

            if part.strip().startswith("title:"):
                filters.append(("title", part.removeprefix("title:").strip()))
            elif part.strip().startswith("text:"):
                filters.append(("text", part.removeprefix("text:").strip()))
            else:
                filters.append(("all", part.strip()))

        results: list[Note] = self.notes
        for filter_type, filter_value in filters:
            if filter_value:
                filtered: list[Note] = []
                filter_value_lower = filter_value.lower()
                for note in results:
                    match filter_type:
                        case "all":
                            if (
                                filter_value_lower in note.title.lower()
                                or filter_value_lower in note.text.lower()
                            ):
                                if note not in filtered:
                                    filtered.append(note)
                            for tag in note.tags:
                                if filter_value_lower in tag.lower():
                                    if note not in filtered:
                                        filtered.append(note)
                                    break
                        case "tag":
                            for tag in note.tags:
                                if filter_value_lower in tag.lower():
                                    if note not in filtered:
                                        filtered.append(note)
                                    break
                        case "title":
                            if filter_value_lower in note.title.lower():
                                if note not in filtered:
                                    filtered.append(note)
                        case "text":
                            if filter_value_lower in note.text.lower():
                                if note not in filtered:
                                    filtered.append(note)
                        case _:
                            continue
                results = filtered
        return results
