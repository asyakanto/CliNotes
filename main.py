from app.app import NotesApp
from app.interface import clear_screen, make_cyan, make_red, interface, show_main_menu
import logging
from prompt_toolkit import prompt
from app.constants import (
    KEY_SETTINGS,
    SETTING_SHOW_ARCHIVED,
    KEY_TOGGLE_ARCHIVED,
    KEY_SEARCH,
    KEY_CREATE,
    KEY_QUIT,
    ACTION_DELETE,
    ACTION_RESTORE,
    ACTION_UNKNOWN,
    ACTION_CHANGE_TEXT,
    ACTION_CHANGE_TITLE,
    ACTION_ARCHIVE,
    ACTION_QUIT,
    LOG_FILE,
)
from sys import sys


def main() -> None:
    try:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(LOG_FILE),
            ],
        )
    except OSError:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            stream=sys.stderr,
        )

    try:
        app = NotesApp()
        logging.info("Application started")
        while True:
            mode = show_main_menu(app)

            if mode.isdigit() and "." not in mode:
                note = app.get_note(int(mode))
                if note:
                    while True:
                        action = interface(note)

                        if action == ACTION_QUIT:
                            break
                        elif action == ACTION_ARCHIVE:
                            app.archive_note(note)
                        elif action == ACTION_CHANGE_TITLE:
                            new_title = prompt(
                                "New title: ", default=note.title
                            ).strip()
                            app.edit_note(note, new_title, note.text)
                        elif action == ACTION_CHANGE_TEXT:
                            new_text = prompt("New text: ", default=note.text).strip()
                            app.edit_note(note, note.title, new_text)
                        elif action == ACTION_UNKNOWN:
                            print()
                            input(make_red("Wrong action"))
                        elif action == ACTION_RESTORE:
                            app.restore_note(note)
                        elif action == ACTION_DELETE:
                            app.delete_note(note)
                            break

            elif mode == KEY_QUIT:
                logging.info("Application closed")
                clear_screen()
                break

            elif mode == KEY_CREATE:
                title = input(make_cyan("Note Name: ")).strip()
                while not title:
                    print(make_red("Title cannot be empty"))
                    title = input(make_cyan("Note Name: "))
                text = input(make_cyan("Text: "))
                note = app.create_note(title, text)
                interface(note)

            elif mode == KEY_SEARCH:
                pass
            elif mode == KEY_TOGGLE_ARCHIVED:
                app.settings.update(
                    {SETTING_SHOW_ARCHIVED: not app.settings.get(SETTING_SHOW_ARCHIVED)}
                )
                app.storage.save_settings(app.settings)
            elif mode == KEY_SETTINGS:
                pass
    except KeyboardInterrupt:
        logging.info("Application interrupted by user")
    except Exception:
        logging.exception("Fatal error")
        print("An error occurred. Details in the app.log")


if __name__ == "__main__":
    main()
