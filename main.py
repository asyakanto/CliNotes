from app.app import NotesApp
from app.interface import (
    clear_screen,
    make_cyan,
    make_red,
    note_interface,
    main_interface,
    display_notes,
    show_note,
    show_main_menu,
    search_help,
)
import logging
from prompt_toolkit import prompt
from app.constants import (
    KEY_SETTINGS,
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
    FILE_LOG,
    SETTING_SHOW_ARCHIVED,
    UI_PROMPT,
    ACTION_TYPE,
    KEY_SEARCH_HELP,
    KEY_SEARCH_QUIT,
)
import sys
from app.notes import Note


def main() -> None:
    try:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(FILE_LOG),
            ],
        )
    except OSError:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            stream=sys.stderr,
        )

    def open_note(app: NotesApp, note: Note) -> None:
        while True:
            print(show_note(note))
            action: ACTION_TYPE = note_interface(note)

            if action == ACTION_QUIT:
                break
            elif action == ACTION_ARCHIVE:
                app.archive_note(note)
            elif action == ACTION_CHANGE_TITLE:
                new_title = prompt("New title: ", default=note.title).strip()
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

    try:
        app: NotesApp = NotesApp()
        logging.info("Application started")
        while True:
            print(show_main_menu(app))
            mode: str = main_interface(app)

            if mode.isdigit() and "." not in mode:
                created_note: Note | None = app.get_note(int(mode))
                if created_note:
                    open_note(app, created_note)

            elif mode == KEY_QUIT:
                logging.info("Application closed")
                clear_screen()
                break

            elif mode == KEY_CREATE:
                title: str = input(make_cyan("Note Name: ")).strip()
                while not title:
                    print(make_red("Title cannot be empty"))
                    title = input(make_cyan("Note Name: "))
                text: str = input(make_cyan("Text: "))
                note: Note = app.create_note(title, text)
                open_note(app, note)

            elif mode == KEY_SEARCH:
                query: str = input(
                    make_cyan(f"Enter a search query ({KEY_SEARCH_HELP} for help): ")
                )
                while query == KEY_SEARCH_HELP:
                    print(search_help())
                    query = input(
                        make_cyan(
                            f"Enter a search query ({KEY_SEARCH_HELP} for help): "
                        )
                    )
                if query == KEY_SEARCH_QUIT:
                    continue
                results: list[Note] = app.search_note(query)
                if not results:
                    print(make_red("Nothing found"))
                    print()
                    input("press Enter...")
                else:
                    while True:
                        clear_screen()
                        print(display_notes(results, True))
                        print(make_cyan(f"Enter ID to open, {KEY_QUIT} to go back"))
                        note_mode: str = input(UI_PROMPT).lower().strip()
                        if note_mode == "q":
                            break
                        if note_mode.isdigit() and "." not in note_mode:
                            found_note: Note | None = app.get_note(int(note_mode))
                            if found_note in results:
                                open_note(app, found_note)
            elif mode == KEY_TOGGLE_ARCHIVED:
                app.settings.update(
                    {SETTING_SHOW_ARCHIVED: not app.settings.get(SETTING_SHOW_ARCHIVED)}
                )
                app.storage.save_settings(app.settings)
            elif mode == KEY_SETTINGS:
                raise NotImplementedError("Settings menu not implemented yet")

    except KeyboardInterrupt:
        logging.info("Application interrupted by user")
    except Exception:
        logging.exception("Fatal error")
        print("An error occurred. Details in the app.log")


if __name__ == "__main__":
    main()
