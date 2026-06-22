from app.app import NotesApp
from datetime import datetime
from app.notes import get_date, get_tags
from app.interface import clear_screen, make_cyan, display_notes, make_red, interf
import logging

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

        print(display_notes(app.notes, app.settings.get("showArchievedNotes")))

        print()

        print(
            make_cyan(
                "Actions: {ID} - open note; q - quit; c - create; s - search; a - show archieved; , - settings"
            )
        )
        mode = input("> ").strip().lower()

        if mode.isdigit() and "." not in mode:
            note = app.get_note(int(mode))
            if note:
                interface(app, note)

        elif mode == "q":
            logging.info("Application closed")
            clear_screen()
            break

        elif mode == "c":
            title = input(make_cyan("Note Name: "))
            text = input(make_cyan("Text: "))
            tags = get_tags(text)
            tags.insert(0, get_date(datetime.now()))

            note = app.create_note(title, text, tags)
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
                {"showArchievedNotes": not app.settings.get("showArchievedNotes")}
            )
            app.storage.save_settings(app.settings)
        elif mode == ",":
            pass


if __name__ == "__main__":
    main()
