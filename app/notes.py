from app.storage import save_notes
from dataclasses import dataclass


@dataclass
class Note:
    title: str
    text: str
    tags: list[str]
    id: int = None


def valid_notes_id(notes):
    max_id = int(get_max_id(notes))
    ids = set()
    for note in notes:
        if note.id is None or note.id < 0 or note.id in ids or "." in str(note.id):
            max_id += 1
            note.id = max_id
        else:
            ids.add(note.id)
    save_notes(notes)
    return notes


def get_max_id(notes):
    max_id = -1
    for note in notes:
        if note.id is not None and note.id > max_id:
            max_id = note.id
    return max_id


def get_tags(text):
    sims = ["@", "#"]
    tags = []
    for s in sims:
        if s in text:
            current_text = text
            while s in current_text:
                index_of_s = current_text.index(s)
                if index_of_s != 0 and current_text[index_of_s - 1] == "\\":
                    current_text = current_text[index_of_s + 2 :]
                else:
                    current_text = current_text[index_of_s + 1 :]
                    min_word = None
                    for i in sims + [" ", "\n", "\t"]:
                        word = current_text.split(i).pop(0)
                        if min_word:
                            if len(word) < len(min_word):
                                min_word = word
                        else:
                            min_word = word
                    if min_word and min_word not in tags:
                        tags.append(min_word)
                    current_text = current_text[len(min_word) :]
        else:
            continue
    return tags


def get_date(dt):
    return f"{dt.day:02d}-{dt.month:02d}-{dt.year}"


def create_note(notes, title, text, tags, id):
    if not title.strip():
        return None
    note = Note(id=id, title=title, text=text, tags=tags)
    notes.append(note)
    save_notes(notes)
    return note


def delete_note(notes, id):
    for i, note in enumerate(notes):
        if id == note.id:
            notes.pop(i)
            save_notes(notes)
            return True
    return False


def search_notes(notes, search):
    if not search:
        return notes
    search = search.lower()
    found_notes = []
    search_by = "title"
    if search[0] == "@":
        search = search[1:]
        search_by = "tags"
    if search_by == "title":
        for note in notes:
            if search in note.title.lower():
                found_notes.append(note)
    elif search_by == "tags":
        for note in notes:
            for tag in note.tags:
                if search in tag:
                    found_notes.append(note)
                    break
    return found_notes
