from json import dump, load, JSONDecodeError
from os import path


JSON_PATH = path.join(path.dirname(path.dirname(__file__)), "notes.json")


def load_notes():
    from app.notes import Note, valid_notes_id

    try:
        with open(JSON_PATH) as file:
            lib = load(file)
            notes = []
            for note in lib:
                notes.append(Note(**note))
            notes = valid_notes_id(notes)
            return notes
    except FileNotFoundError, JSONDecodeError:
        return []


def save_notes(notes):
    from dataclasses import asdict

    lib = []
    for note in notes:
        lib.append(asdict(note))
    with open(JSON_PATH, "w") as file:
        dump(lib, file)
