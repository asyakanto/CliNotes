import logging
import sys
from collections.abc import Callable

from app.app import NotesApp
from app.constants import Constants as C
from app.models import Note
from app.paths import data_dir
from app.ui_input import pause
from app.ui_menu import display_main_menu
from app.ui_note import open_note
from app.ui_scenarios import create_note_scenario, search_scenario
from app.ui_settings import settings_interface
from app.ui_style import StyleConfig, apply_settings, clear_screen

logger = logging.getLogger(__name__)


def run_app(app: NotesApp, style_config: StyleConfig) -> None:
    action_table: dict[str, Callable[[NotesApp, StyleConfig], None]] = {
        C.KEY_CREATE: create_note_scenario,
        C.KEY_SEARCH: search_scenario,
        C.KEY_SETTINGS: settings_interface,
    }
    while True:
        mode: str = display_main_menu(app, style_config)

        if mode.isdigit():
            created_note: Note | None = app.get_note(int(mode))
            if created_note:
                open_note(app, created_note, style_config)

        elif mode == C.KEY_QUIT:
            logger.info("Application closed")
            clear_screen(style_config)
            app.save_notes()
            return
        elif mode == C.KEY_TOGGLE_ARCHIVED:
            app.toggle_show_archived()
        elif mode in action_table:
            action_table[mode](app, style_config)


def main() -> None:
    try:
        data_dir().mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(data_dir() / C.FILE_LOG),
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
        style_config: StyleConfig = StyleConfig()
        apply_settings(app, style_config, start=True)
        logger.info("Application started")
    except KeyboardInterrupt:
        logger.info(
            "Application interrupted by user during startup. Notes were not saved"
        )
        return
    except Exception:
        logger.exception("Fatal error")
        pause(f"An error occurred. Details in the {C.FILE_LOG}", style_config)
        return

    try:
        run_app(app, style_config)
    except KeyboardInterrupt:
        app.save_notes()
        logger.info("Application interrupted by user")
        return
    except Exception:
        logger.exception("Fatal error")
        pause(f"An error occurred. Details in the {C.FILE_LOG}", style_config)
        return
