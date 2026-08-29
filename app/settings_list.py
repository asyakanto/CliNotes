from app.constants import Constants as C
from app.paths import data_dir


class Setting:
    def __init__(
        self,
        key: str,
        label: str,
        field_type: str,
        default: int | bool | str,
        group: str,
        order: int,
        options: list[str | int] | None = None,
        min_value: int | None = None,
        max_value: int | None = None,
        max_length: int | None = None,
        value: int | bool | str | None = None,
    ) -> None:
        self.key = key
        self.label = label
        self.field_type = field_type
        self.value = value if value is not None else default
        self.default = default
        self.group = group
        self.order = order
        self.options = options if options is not None else []
        self.min_value = min_value
        self.max_value = max_value
        self.max_length = max_length

    def validate(self, value: bool | str | int) -> bool:
        return (
            (self.field_type == C.FIELD_TYPE_BOOL and isinstance(value, bool))
            or (
                self.field_type == C.FIELD_TYPE_STR
                and isinstance(value, str)
                and (self.max_length is None or len(value) <= self.max_length)
            )
            or (
                self.field_type == C.FIELD_TYPE_INT
                and not isinstance(value, bool)
                and isinstance(value, int)
                and (self.min_value is None or value >= self.min_value)
                and (self.max_value is None or value <= self.max_value)
            )
            or (
                self.field_type == C.FIELD_TYPE_CHOICE
                and (value in self.options)
                and not isinstance(value, bool)
            )
        )


def build_default_settings() -> list[Setting]:
    return [
        Setting(
            key=C.SETTING_SHOW_ARCHIVED,
            label="Show archived notes",
            field_type=C.FIELD_TYPE_BOOL,
            default=False,
            group=C.GROUP_DISPLAY,
            order=1,
        ),
        Setting(
            key=C.DATE_FORMAT_SETTING,
            label="Date format",
            field_type=C.FIELD_TYPE_CHOICE,
            default="DD-MM-YYYY",
            group=C.GROUP_DISPLAY,
            order=2,
            options=list(C.DATE_FORMAT_MAP.keys()),
        ),
        Setting(
            key=C.SETTING_AUTO_DELETE_DAYS,
            label="Days before auto deleting archived notes",
            field_type=C.FIELD_TYPE_INT,
            default=30,
            group=C.GROUP_ARCHIVING,
            order=1,
            min_value=1,
        ),
        Setting(
            key=C.SETTING_CONFIRM_ARCHIVE,
            label="Confirm before archiving note",
            field_type=C.FIELD_TYPE_BOOL,
            default=False,
            group=C.GROUP_ARCHIVING,
            order=2,
        ),
        Setting(
            key=C.SETTING_CONFIRM_DELETE,
            label="Confirm before deleting note",
            field_type=C.FIELD_TYPE_BOOL,
            default=True,
            group=C.GROUP_ARCHIVING,
            order=3,
        ),
        Setting(
            key=C.SETTING_AUTO_SYNC_TAGS,
            order=1,
            label="Auto-sync note tags",
            field_type=C.FIELD_TYPE_BOOL,
            default=True,
            group=C.GROUP_CREATING,
        ),
        Setting(
            key=C.SETTING_AUTO_DATE_TAG,
            label="Add date tag to notes",
            field_type=C.FIELD_TYPE_BOOL,
            default=True,
            group=C.GROUP_CREATING,
            order=2,
        ),
        Setting(
            key=C.SETTING_DEFAULT_TEXT,
            label="Default text for empty note",
            field_type=C.FIELD_TYPE_STR,
            default="-",
            group=C.GROUP_CREATING,
            order=3,
        ),
        Setting(
            key=C.SETTING_USE_AT,
            label=f"Use {C.TAG_PREFIX_SETTINGS[C.SETTING_USE_AT]} tag prefix",
            field_type=C.FIELD_TYPE_BOOL,
            default=True,
            group=C.GROUP_CREATING,
            order=4,
        ),
        Setting(
            key=C.SETTING_USE_HASH,
            label=f"Use {C.TAG_PREFIX_SETTINGS[C.SETTING_USE_HASH]} tag prefix",
            field_type=C.FIELD_TYPE_BOOL,
            default=True,
            group=C.GROUP_CREATING,
            order=5,
        ),
        Setting(
            key=C.SETTING_USE_TAG_COLON,
            label=f"Use {C.TAG_PREFIX_SETTINGS[C.SETTING_USE_TAG_COLON]} tag prefix",
            field_type=C.FIELD_TYPE_BOOL,
            default=True,
            group=C.GROUP_CREATING,
            order=6,
        ),
        Setting(
            key=C.SETTING_USE_EXCLAMATION,
            label=f"Use {C.TAG_PREFIX_SETTINGS[C.SETTING_USE_EXCLAMATION]} tag prefix",
            field_type=C.FIELD_TYPE_BOOL,
            default=False,
            group=C.GROUP_CREATING,
            order=7,
        ),
        Setting(
            key=C.SETTING_USE_DOLLAR,
            label=f"Use {C.TAG_PREFIX_SETTINGS[C.SETTING_USE_DOLLAR]} tag prefix",
            field_type=C.FIELD_TYPE_BOOL,
            default=False,
            group=C.GROUP_CREATING,
            order=8,
        ),
        Setting(
            key=C.SETTING_USE_PLUS,
            label=f"Use {C.TAG_PREFIX_SETTINGS[C.SETTING_USE_PLUS]} tag prefix",
            field_type=C.FIELD_TYPE_BOOL,
            default=False,
            group=C.GROUP_CREATING,
            order=9,
        ),
        Setting(
            key=C.SETTING_USE_AMPERSAND,
            label=f"Use {C.TAG_PREFIX_SETTINGS[C.SETTING_USE_AMPERSAND]} tag prefix",
            field_type=C.FIELD_TYPE_BOOL,
            default=False,
            group=C.GROUP_CREATING,
            order=10,
        ),
        Setting(
            key=C.SETTING_USE_PERCENT,
            label=f"Use {C.TAG_PREFIX_SETTINGS[C.SETTING_USE_PERCENT]} tag prefix",
            field_type=C.FIELD_TYPE_BOOL,
            default=False,
            group=C.GROUP_CREATING,
            order=11,
        ),
        Setting(
            key=C.SETTING_USE_COLORS,
            label="Colored output",
            field_type=C.FIELD_TYPE_BOOL,
            default=True,
            group=C.GROUP_INTERFACE,
            order=1,
        ),
        Setting(
            key=C.SETTING_USE_CLEAR_SCREEN,
            label="Clear screen",
            field_type=C.FIELD_TYPE_BOOL,
            default=True,
            group=C.GROUP_INTERFACE,
            order=2,
        ),
        Setting(
            key=C.SETTING_USE_HINTS,
            label="Show hints",
            field_type=C.FIELD_TYPE_BOOL,
            default=True,
            group=C.GROUP_INTERFACE,
            order=3,
        ),
        Setting(
            key=C.SETTING_NOTES_PATH,
            label="Notes file path",
            field_type=C.FIELD_TYPE_STR,
            default=str(data_dir()),
            order=1,
            group=C.GROUP_SYSTEM,
        ),
        Setting(
            key=C.SETTING_LOG_LEVEL,
            label="Log level",
            field_type=C.FIELD_TYPE_CHOICE,
            default="low",
            group=C.GROUP_SYSTEM,
            order=2,
            options=list(C.LOG_LEVELS),
        ),
        Setting(
            key=C.SETTING_AUTO_SAVE,
            label="Autosave",
            field_type=C.FIELD_TYPE_BOOL,
            default=True,
            order=3,
            group=C.GROUP_SYSTEM,
        ),
    ]
