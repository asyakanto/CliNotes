from typing import Final, Literal


class Constants:
    # ── ANSI Colors ──────────────────────────
    ANSI_RESET: Final = "\033[0m"
    ANSI_RED: Final = "\033[31m"
    ANSI_CYAN: Final = "\033[36m"
    ANSI_DIM: Final = "\033[2m"

    # ── Files ────────────────────────────────
    FILE_NOTES: Final = "notes.json"
    FILE_SETTINGS: Final = "settings.json"
    FILE_LOG: Final = "app.log"

    # ── Defaults ─────────────────────────────
    DEFAULT_ARCHIVED_AT: Final = "0"
    DEFAULT_TEXT: Final = "-"
    AUTO_DELETE_DAYS: Final = 30
    DEFAULT_TERMINAL_WIDTH: Final = 80

    # ── UI ───────────────────────────────────
    UI_PROMPT: Final = "> "

    # ── Keys (главное меню) ─────────────────
    KEY_QUIT: Final = "q"
    KEY_CREATE: Final = "c"
    KEY_SEARCH: Final = "s"
    KEY_TOGGLE_ARCHIVED: Final = "t"
    KEY_SETTINGS: Final = ","

    # ── Keys (меню заметки) ─────────────────
    KEY_ARCHIVE: Final = "a"
    KEY_EDIT: Final = "e"
    KEY_EDIT_TITLE: Final = "t"
    KEY_EDIT_TEXT: Final = "i"
    KEY_RESTORE: Final = "r"
    KEY_DELETE: Final = "d"

    # ── Actions ──────────────────────────────
    ACTION_QUIT: Final = "quit"
    ACTION_ARCHIVE: Final = "archive"
    ACTION_CHANGE_TITLE: Final = "change title"
    ACTION_CHANGE_TEXT: Final = "change text"
    ACTION_RESTORE: Final = "restore"
    ACTION_DELETE: Final = "delete"
    ACTION_UNKNOWN: Final = "unknown"
    ACTION_TYPE = Literal[
        "quit", "archive", "change title", "change text", "restore", "delete", "unknown"
    ]

    # ── Tags ─────────────────────────────────
    TAG_PREFIXES: Final[list[str]] = ["@", "#", "tag:"]

    # ── IDs ──────────────────────────────────
    NO_NOTES_MAX_ID: Final = -1

    SETTING_SHOW_ARCHIVED: Final = "show_archived_notes"
    DATE_FORMAT_SETTING: Final = "date_format"

    # ── Search ─────────────────────────────
    KEY_SEARCH_HELP: Final = "%h"
    KEY_SEARCH_QUIT: Final = "%q"

    # ── Dates ────────────────────────────────
    DATE_FORMAT_MAP: Final = {
        "DD-MM-YYYY": "%d-%m-%Y",
        "DD.MM.YYYY": "%d.%m.%Y",
        "DD/MM/YYYY": "%d/%m/%Y",
        "DD MM YYYY": "%d %m %Y",
        "MM-DD-YYYY": "%m-%d-%Y",
        "MM.DD.YYYY": "%m.%d.%Y",
        "MM/DD/YYYY": "%m/%d/%Y",
        "MM DD YYYY": "%m %d %Y",
        "YYYY-MM-DD": "%Y-%m-%d",
        "YYYY.MM.DD": "%Y.%m.%d",
        "YYYY/MM/DD": "%Y/%m/%d",
        "YYYY MM DD": "%Y %m %d",
        "DD-MM-YY": "%d-%m-%y",
        "DD.MM.YY": "%d.%m.%y",
        "DD/MM/YY": "%d/%m/%y",
        "DD MM YY": "%d %m %y",
        "MM-DD-YY": "%m-%d-%y",
        "MM.DD.YY": "%m.%d.%y",
        "MM/DD/YY": "%m/%d/%y",
        "MM DD YY": "%m %d %y",
        "YY-MM-DD": "%y-%m-%d",
        "YY.MM.DD": "%y.%m.%d",
        "YY/MM/DD": "%y/%m/%d",
        "YY MM DD": "%y %m %d",
    }

    DATE_FORMAT_STORAGE: Final = "%d-%m-%Y"
