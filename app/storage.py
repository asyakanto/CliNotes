from json import dump, load, JSONDecodeError
from os import path

class Storage:
    def __init__(self):
        self.JSON_PATH = path.join(path.dirname(path.dirname(__file__)), "notes.json")
    
    def load(self):
        try:
            with open(self.JSON_PATH) as file:
                return load(file)
        except (FileNotFoundError, JSONDecodeError):
            return []

    def save (self, notes):
        from dataclasses import asdict

        lib = []
        for note in notes:
            lib.append(asdict(note))
        with open(self.JSON_PATH, "w") as file:
            dump(lib, file)