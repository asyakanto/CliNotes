# ── ANSI Colors ──────────────────────────
ANSI_RESET = "\033[0m"
ANSI_RED = "\033[31m"
ANSI_CYAN = "\033[36m"
ANSI_DIM = "\033[2m"

# ── Files ────────────────────────────────
FILE_NOTES = "notes.json"
FILE_SETTINGS = "settings.json"
FILE_LOG = "app.log"

# ── Date ─────────────────────────────────
DATE_FORMAT = "%d-%m-%Y"

# ── Defaults ─────────────────────────────
DEFAULT_ARCHIVED_AT = "0"
DEFAULT_TEXT = "-"
AUTO_DELETE_DAYS = 30

# ── UI ───────────────────────────────────
UI_PROMPT = "> "
UI_SEPARATOR_WIDTH = 15

# ── Keys (главное меню) ─────────────────
KEY_QUIT = "q"
KEY_CREATE = "c"
KEY_SEARCH = "s"
KEY_TOGGLE_ARCHIVED = "a"
KEY_SETTINGS = ","

# ── Keys (меню заметки) ─────────────────
KEY_ARCHIVE = "a"
KEY_EDIT = "e"
KEY_EDIT_TITLE = "t"
KEY_EDIT_TEXT = "i"
KEY_RESTORE = "r"
KEY_DELETE = "d"

# ── Actions ──────────────────────────────
ACTION_QUIT = "quit"
ACTION_ARCHIVE = "archive"
ACTION_CHANGE_TITLE = "change title"
ACTION_CHANGE_TEXT = "change text"
ACTION_RESTORE = "restore"
ACTION_DELETE = "delete"
ACTION_UNKNOWN = "unknown"

# ── Settings ─────────────────────────────
SETTING_SHOW_ARCHIVED = "showArchivedNotes"

# ── Tags ─────────────────────────────────
TAG_PREFIXES = ["@", "#"]
TAG_SEPARATORS = [" ", "\n", "\t"]

# ── IDs ──────────────────────────────────
NO_NOTES_MAX_ID = -1
