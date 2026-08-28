import logging
from typing import Final, Literal


class Constants:
    # ── ANSI Colors ──────────────────────────
    ANSI_RESET: Final[str] = "\033[0m"
    ANSI_RED: Final[str] = "\033[31m"
    ANSI_CYAN: Final[str] = "\033[36m"
    ANSI_DIM: Final[str] = "\033[2m"
    ANSI_PINK: Final[str] = "\033[38;5;213m"

    # ── Files ────────────────────────────────
    FILE_NOTES: Final[str] = "notes.json"
    FILE_SETTINGS: Final[str] = "settings.json"
    FILE_LOG: Final[str] = "app.log"
    FILE_TEMP: Final[str] = "temp.json"
    TEMP_SETTINGS_FILE: Final[str] = "tempSettings.json"

    # ── Defaults ─────────────────────────────
    DEFAULT_ARCHIVED_AT: Final[str] = "0"
    DEFAULT_TERMINAL_WIDTH: Final[int] = 80

    # ── UI ───────────────────────────────────
    UI_PROMPT: Final[str] = "> "
    EASTER_EGG: Final[str] = "<3"
    EASTER_EGG_CONDITIONS: Final[list[str]] = ["asya", "kanto"]

    # ── Keys (главное меню) ─────────────────
    KEY_QUIT: Final[str] = "q"
    KEY_CREATE: Final[str] = "c"
    KEY_SEARCH: Final[str] = "s"
    KEY_TOGGLE_ARCHIVED: Final[str] = "t"
    KEY_SETTINGS: Final[str] = ","

    # ── Keys ────────────────────────────────
    KEY_ARCHIVE: Final[str] = "a"
    KEY_EDIT: Final[str] = "e"
    KEY_EDIT_TITLE: Final[str] = "t"
    KEY_EDIT_TEXT: Final[str] = "i"
    KEY_RESTORE: Final[str] = "r"
    KEY_DELETE: Final[str] = "d"
    KEY_PERCENT_QUIT: Final[str] = "%q"

    # ── Actions ──────────────────────────────
    ACTION_QUIT: Final = "quit"
    ACTION_ARCHIVE: Final = "archive"
    ACTION_CHANGE_TITLE: Final = "change title"
    ACTION_CHANGE_TEXT: Final = "change text"
    ACTION_RESTORE: Final = "restore"
    ACTION_DELETE: Final = "delete"
    ACTION_UNKNOWN: Final = "unknown"
    ACTION_TYPE = Literal[
        "quit",
        "archive",
        "change title",
        "change text",
        "restore",
        "delete",
        "unknown",
    ]

    # ── IDs ──────────────────────────────────
    NO_NOTES_MAX_ID: Final = -1

    # ── Settings ─────────────────────────────

    KEY_RESET_SETTINGS: Final[str] = "r"

    SETTING_SHOW_ARCHIVED: Final[str] = "show_archived_notes"
    DATE_FORMAT_SETTING: Final[str] = "date_format"
    SETTING_AUTO_DELETE_DAYS: Final[str] = "auto_delete_days"
    SETTING_CONFIRM_ARCHIVE: Final[str] = "confirm_archive"
    SETTING_CONFIRM_DELETE: Final[str] = "confirm_delete"
    SETTING_AUTO_DATE_TAG: Final[str] = "auto_date_tag"
    SETTING_USE_AT: Final[str] = "use_@"
    SETTING_USE_HASH: Final[str] = "use_#"
    SETTING_USE_TAG_COLON: Final[str] = "use_tag:"
    SETTING_USE_EXCLAMATION: Final[str] = "use_!"
    SETTING_USE_DOLLAR: Final[str] = "use_$"
    SETTING_USE_PLUS: Final[str] = "use_+"
    SETTING_USE_AMPERSAND: Final[str] = "use_&"
    SETTING_USE_PERCENT: Final[str] = "use_%"
    TAG_PREFIX_SETTINGS: Final[dict[str, str]] = {
        SETTING_USE_AT: "@",
        SETTING_USE_HASH: "#",
        SETTING_USE_TAG_COLON: "tag:",
        SETTING_USE_EXCLAMATION: "!",
        SETTING_USE_DOLLAR: "$",
        SETTING_USE_PLUS: "+",
        SETTING_USE_AMPERSAND: "&",
        SETTING_USE_PERCENT: "%",
    }
    SETTING_DEFAULT_TEXT: Final[str] = "default_text"
    SETTING_USE_COLORS: Final[str] = "use_colors"
    SETTING_USE_CLEAR_SCREEN: Final[str] = "use_clear_screen"
    SETTING_USE_HINTS: Final[str] = "use_hints"
    SETTING_AUTO_SYNC_TAGS: Final[str] = "auto_sync_tags"
    SETTING_NOTES_PATH: Final[str] = "notes_path"
    SETTING_LOG_LEVEL: Final[str] = "log_level"
    SETTING_AUTO_SAVE: Final[str] = "auto_save"
    LOG_LEVELS: Final[list[str]] = ["off", "low", "high"]
    LOG_OFF: Final[int] = logging.CRITICAL + 1
    LOG_LEVEL_MAP: Final[dict[str, int]] = {
        LOG_LEVELS[0]: LOG_OFF,
        LOG_LEVELS[1]: logging.ERROR,
        LOG_LEVELS[2]: logging.DEBUG,
    }

    # ── Search ─────────────────────────────
    KEY_SEARCH_HELP: Final[str] = "%h"

    # ── Dates ────────────────────────────────
    DATE_FORMAT_MAP: Final[dict[str, str]] = {
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

    DATE_FORMAT_STORAGE: Final[str] = "%d-%m-%Y"
