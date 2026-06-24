from app.app import NotesApp
from datetime import datetime
from app.notes import get_date, get_tags
from app.interface import clear_screen, make_cyan, display_notes, make_red, interface
import logging
from prompt_toolkit import prompt

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
    ],
)


def main() -> None:
    app = NotesApp()
    logging.info("Application started")
    while True:
        clear_screen()
        print(make_red("CliNotes") + ": " + get_date(datetime.now()))
        print()

        print(display_notes(app.notes, app.settings.get("showArchivedNotes")))

        print()

        print(
            make_cyan(
                "Actions: {ID} - open note; q - quit; c - create; s - search; a - show archived; , - settings"
            )
        )
        mode = input("> ").strip().lower()

        if mode.isdigit() and "." not in mode:
            note = app.get_note(int(mode))
            if note:
                while True:
                    action = interface(app, note)

                    if action == "quit":
                        break
                    elif action == "archive":
                        app.archive_note(note)
                    elif action == "change title":
                        new_title = prompt("New title: ", default=note.title).strip()
                        app.edit_note(note, new_title, note.text)
                    elif action == "change text":
                        new_text = prompt("New text: ", default=note.text).strip()
                        app.edit_note(note, note.title, new_text)
                    elif action == "unknown":
                        print()
                        input(make_red("Wrong action"))
                    elif action == "restore":
                        app.restore_note(note)
                    elif action == "delete":
                        app.delete_note(note)
                        break

        elif mode == "q":
            logging.info("Application closed")
            clear_screen()
            break

        elif mode == "c":
            title = input(make_cyan("Note Name: "))
            text = input(make_cyan("Text: "))
            tags = get_tags(text)
            created = get_date(datetime.now())
            tags.insert(0, created)

            note = app.create_note(title, text, tags, created)
            print()

            while note is None:
                print(make_red("Title cannot be empty"))
                title = input(make_cyan("Note Name: "))
                note = app.create_note(title, text, tags)
                print()
            interface(app, note)

        elif mode == "s":
            pass
        elif mode == "a":
            app.settings.update(
                {"showArchivedNotes": not app.settings.get("showArchivedNotes")}
            )
            app.storage.save_settings(app.settings)
        elif mode == ",":
            pass


if __name__ == "__main__":
    main()
