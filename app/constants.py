from typing import Literal, Final

# ── ANSI Colors ──────────────────────────
ANSI_RESET: Final = "\033[0m"
ANSI_RED: Final = "\033[31m"
ANSI_CYAN: Final = "\033[36m"
ANSI_DIM: Final = "\033[2m"

# ── Files ────────────────────────────────
FILE_NOTES: Final = "notes.json"
FILE_SETTINGS: Final = "settings.json"
FILE_LOG: Final = "app.log"

# ── Date ─────────────────────────────────
DATE_FORMAT: Final = "%d-%m-%Y"

# ── Defaults ─────────────────────────────
DEFAULT_ARCHIVED_AT: Final = "0"
DEFAULT_TEXT: Final = "-"
AUTO_DELETE_DAYS: Final = 30

# ── UI ───────────────────────────────────
UI_PROMPT: Final = "> "
UI_SEPARATOR_WIDTH: Final = 15

# ── Keys (главное меню) ─────────────────
KEY_QUIT: Final = "q"
KEY_CREATE: Final = "c"
KEY_SEARCH: Final = "s"
KEY_TOGGLE_ARCHIVED: Final = "a"
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

# ── Settings ─────────────────────────────
SETTING_SHOW_ARCHIVED: Final = "showArchivedNotes"

# ── Tags ─────────────────────────────────
TAG_PREFIXES: Final[list[str]] = ["@", "#", "tag:"]
TAG_SEPARATORS: Final[list[str]] = [" ", "\n", "\t"]

# ── IDs ──────────────────────────────────
NO_NOTES_MAX_ID: Final = -1
