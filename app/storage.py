from json import dump, load, JSONDecodeError
from os import path

JSON_PATH = path.join(path.dirname(path.dirname(__file__)), "notes.json")

def load_notes():
    try:
        with open(JSON_PATH) as file:
            return load(file)
    except (FileNotFoundError, JSONDecodeError):
        return []

def save_notes(notes):
    with open(JSON_PATH, "w") as file:
        dump(notes, file)