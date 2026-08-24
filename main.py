import logging
import sys

from app.app import NotesApp
from app.constants import Constants as C
from app.models import Note
from app.ui_input import pause
from app.ui_menu import display_main_menu
from app.ui_note import open_note
from app.ui_scenarios import create_note_scenario, search_scenario
from app.ui_settings import settings_interface
from app.ui_style import (
    apply_settings,
    clear_screen,
)

logger = logging.getLogger(__name__)


def run_app(app: NotesApp) -> None:
    while True:
        mode: str = display_main_menu(app)

        if mode.isdigit():
            created_note: Note | None = app.get_note(int(mode))
            if created_note:
                open_note(app, created_note)

        elif mode == C.KEY_QUIT:
            logger.info("Application closed")
            clear_screen()
            app.save_notes()
            return

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
        apply_settings(app)
        logger.info("Application started")
    except KeyboardInterrupt:
        logger.info(
            "Application interrupted by user during startup. Notes were not saved"
        )
        return
    except Exception:
        logger.exception("Fatal error")
        pause("An error occurred. Details in the app.log")
        return

    try:
        run_app(app)
    except KeyboardInterrupt:
        app.save_notes()
        logger.info("Application interrupted by user")
        return
    except Exception:
        logger.exception("Fatal error")
        pause("An error occurred. Details in the app.log")
        return


if __name__ == "__main__":
    main()
