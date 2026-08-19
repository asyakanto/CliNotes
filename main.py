import logging
import sys

from app.app import NotesApp
from app.constants import Constants as C
from app.interface import (
    clear_screen,
    create_note_scenario,
    display_main_menu,
    open_note,
    search_scenario,
    set_clear_screen_enabled,
    set_colors_enabled,
    set_hints_enabled,
    settings_interface,
    show_fatal_error,
)
from app.models import Note

logger = logging.getLogger(__name__)


def main() -> None:
    try:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(C.FILE_LOG),
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
        set_colors_enabled(app.settings.get_bool_value(C.SETTING_USE_COLORS))
        set_clear_screen_enabled(
            app.settings.get_bool_value(C.SETTING_USE_CLEAR_SCREEN)
        )
        set_hints_enabled(app.settings.get_bool_value(C.SETTING_USE_HINTS))
        logger.info("Application started")
        while True:
            mode: str = display_main_menu(app)

            if mode.isdigit() and "." not in mode:
                created_note: Note | None = app.get_note(int(mode))
                if created_note:
                    open_note(app, created_note)

            elif mode == C.KEY_QUIT:
                logger.info("Application closed")
                clear_screen()
                break

            elif mode == C.KEY_CREATE:
                create_note_scenario(app)

            elif mode == C.KEY_SEARCH:
                search_scenario(app)
            elif mode == C.KEY_TOGGLE_ARCHIVED:
                app.settings.set_value(
                    C.SETTING_SHOW_ARCHIVED,
                    not app.settings.get_bool_value(C.SETTING_SHOW_ARCHIVED),
                )
                app.save_settings()
            elif mode == C.KEY_SETTINGS:
                settings_interface(app)

    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception:
        logger.exception("Fatal error")
        show_fatal_error()


if __name__ == "__main__":
    main()
