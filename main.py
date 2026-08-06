import logging
import sys

from app.app import NotesApp
from app.constants import (
    FILE_LOG,
    KEY_CREATE,
    KEY_QUIT,
    KEY_SEARCH,
    KEY_SEARCH_HELP,
    KEY_SEARCH_QUIT,
    KEY_SETTINGS,
    KEY_TOGGLE_ARCHIVED,
    SETTING_SHOW_ARCHIVED,
    UI_PROMPT,
)
from app.interface import (
    clear_screen,
    display_notes,
    main_interface,
    make_cyan,
    make_red,
    open_note,
    show_main_menu,
)
from app.models import Note
from app.search import search_help

logger = logging.getLogger(__name__)


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

    try:
        app: NotesApp = NotesApp()
        logger.info("Application started")
        while True:
            clear_screen()
            print(show_main_menu(app))
            mode: str = main_interface(app)

            if mode.isdigit() and "." not in mode:
                created_note: Note | None = app.get_note(int(mode))
                if created_note:
                    open_note(app, created_note)

            elif mode == KEY_QUIT:
                logger.info("Application closed")
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
                        if note_mode == KEY_QUIT:
                            break
                        if note_mode.isdigit() and "." not in note_mode:
                            found_note: Note | None = app.get_note(int(note_mode))
                            if found_note in results:
                                open_note(app, found_note)
            elif mode == KEY_TOGGLE_ARCHIVED:
                app.settings.update(
                    {
                        SETTING_SHOW_ARCHIVED: not app.settings.get(
                            SETTING_SHOW_ARCHIVED, False
                        )
                    }
                )
                app.storage.save_settings(app.settings)
            elif mode == KEY_SETTINGS:
                raise NotImplementedError("Settings menu not implemented yet")

    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception:
        logger.exception("Fatal error")
        print("An error occurred. Details in the app.log")


if __name__ == "__main__":
    main()
