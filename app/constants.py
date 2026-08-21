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

    # ── IDs ──────────────────────────────────
    NO_NOTES_MAX_ID: Final = -1

    # ── Settings ─────────────────────────────

    KEY_RESET_SETTINGS: Final = "r"

    SETTING_SHOW_ARCHIVED: Final = "show_archived_notes"
    DATE_FORMAT_SETTING: Final = "date_format"
    SETTING_AUTO_DELETE_DAYS: Final = "auto_delete_days"
    SETTING_CONFIRM_ARCHIVE: Final = "confirm_archive"
    SETTING_CONFIRM_DELETE: Final = "confirm_delete"
    SETTING_AUTO_DATE_TAG: Final = "auto_date_tag"
    SETTING_USE_AT: Final = "use_@"
    SETTING_USE_HASH: Final = "use_#"
    SETTING_USE_TAG_COLON: Final = "use_tag:"
    SETTING_USE_EXCLAMATION: Final = "use_!"
    SETTING_USE_DOLLAR: Final = "use_$"
    SETTING_USE_PLUS: Final = "use_+"
    SETTING_USE_AMPERSAND: Final = "use_&"
    SETTING_USE_PERCENT: Final = "use_%"
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
    SETTING_DEFAULT_TEXT: Final = "default_text"
    SETTING_USE_COLORS: Final = "use_colors"
    SETTING_USE_CLEAR_SCREEN: Final = "use_clear_screen"
    SETTING_USE_HINTS: Final = "use_hints"
    SETTING_AUTO_SYNC_TAGS: Final = "auto_sync_tags"
    SETTING_NOTES_PATH: Final = "notes_path"
    SETTING_LOG_LEVEL: Final = "log_level"
    SETTING_AUTO_SAVE: Final = "auto_save"
    LOG_LEVELS: Final = ["off", "low", "high"]

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
