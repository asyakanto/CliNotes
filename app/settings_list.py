"""Settings definition: the Setting dataclass and default settings."""

from dataclasses import dataclass, field

from app.constants import Constants
from app.paths import data_dir


@dataclass
class Setting:
    """A single configurable setting with type, bounds and value."""

    key: str
    label: str
    field_type: str
    default: int | bool | str
    group: str
    order: int
    options: list[str | int] = field(default_factory=list)
    min_value: int | None = None
    max_value: int | None = None
    max_length: int | None = None
    value: int | bool | str | None = None

    def __post_init__(self) -> None:
        """Use the default value when no value was provided."""
        if self.value is None:
            self.value = self.default

    def validate(self, value: bool | str | int) -> bool:  # noqa: FBT001
        """Return whether the value matches this setting's type and bounds."""
        return (
            (self.field_type == Constants.FIELD_TYPE_BOOL and isinstance(value, bool))
            or (
                self.field_type == Constants.FIELD_TYPE_STR
                and isinstance(value, str)
                and (self.max_length is None or len(value) <= self.max_length)
            )
            or (
                self.field_type == Constants.FIELD_TYPE_INT
                and not isinstance(value, bool)
                and isinstance(value, int)
                and (self.min_value is None or value >= self.min_value)
                and (self.max_value is None or value <= self.max_value)
            )
            or (
                self.field_type == Constants.FIELD_TYPE_CHOICE
                and (value in (self.options or []))
                and not isinstance(value, bool)
            )
        )


def build_default_settings() -> list[Setting]:
    """Build the default list of application settings."""
    return [
        Setting(
            key=Constants.SETTING_SHOW_ARCHIVED,
            label="Show archived notes",
            field_type=Constants.FIELD_TYPE_BOOL,
            default=False,
            group=Constants.GROUP_DISPLAY,
            order=1,
        ),
        Setting(
            key=Constants.DATE_FORMAT_SETTING,
            label="Date format",
            field_type=Constants.FIELD_TYPE_CHOICE,
            default="DD-MM-YYYY",
            group=Constants.GROUP_DISPLAY,
            order=2,
            options=list(Constants.DATE_FORMAT_MAP.keys()),
        ),
        Setting(
            key=Constants.SETTING_AUTO_DELETE_DAYS,
            label="Days before auto deleting archived notes",
            field_type=Constants.FIELD_TYPE_INT,
            default=30,
            group=Constants.GROUP_ARCHIVING,
            order=1,
            min_value=1,
        ),
        Setting(
            key=Constants.SETTING_CONFIRM_ARCHIVE,
            label="Confirm before archiving note",
            field_type=Constants.FIELD_TYPE_BOOL,
            default=False,
            group=Constants.GROUP_ARCHIVING,
            order=2,
        ),
        Setting(
            key=Constants.SETTING_CONFIRM_DELETE,
            label="Confirm before deleting note",
            field_type=Constants.FIELD_TYPE_BOOL,
            default=True,
            group=Constants.GROUP_ARCHIVING,
            order=3,
        ),
        Setting(
            key=Constants.SETTING_AUTO_SYNC_TAGS,
            order=1,
            label="Auto-sync note tags",
            field_type=Constants.FIELD_TYPE_BOOL,
            default=True,
            group=Constants.GROUP_CREATING,
        ),
        Setting(
            key=Constants.SETTING_AUTO_DATE_TAG,
            label="Add date tag to notes",
            field_type=Constants.FIELD_TYPE_BOOL,
            default=True,
            group=Constants.GROUP_CREATING,
            order=2,
        ),
        Setting(
            key=Constants.SETTING_DEFAULT_TEXT,
            label="Default text for empty note",
            field_type=Constants.FIELD_TYPE_STR,
            default="-",
            group=Constants.GROUP_CREATING,
            order=3,
        ),
        Setting(
            key=Constants.SETTING_USE_AT,
            label=f"Use "
            f"{Constants.TAG_PREFIX_SETTINGS[Constants.SETTING_USE_AT]}"
            f" tag prefix",
            field_type=Constants.FIELD_TYPE_BOOL,
            default=True,
            group=Constants.GROUP_CREATING,
            order=4,
        ),
        Setting(
            key=Constants.SETTING_USE_HASH,
            label=f"Use "
            f"{Constants.TAG_PREFIX_SETTINGS[Constants.SETTING_USE_HASH]}"
            " tag prefix",
            field_type=Constants.FIELD_TYPE_BOOL,
            default=True,
            group=Constants.GROUP_CREATING,
            order=5,
        ),
        Setting(
            key=Constants.SETTING_USE_TAG_COLON,
            label=f"Use "
            f"{Constants.TAG_PREFIX_SETTINGS[Constants.SETTING_USE_TAG_COLON]}"
            f" tag prefix",
            field_type=Constants.FIELD_TYPE_BOOL,
            default=True,
            group=Constants.GROUP_CREATING,
            order=6,
        ),
        Setting(
            key=Constants.SETTING_USE_EXCLAMATION,
            label=f"Use "
            f"{Constants.TAG_PREFIX_SETTINGS[Constants.SETTING_USE_EXCLAMATION]}"
            f" tag prefix",
            field_type=Constants.FIELD_TYPE_BOOL,
            default=False,
            group=Constants.GROUP_CREATING,
            order=7,
        ),
        Setting(
            key=Constants.SETTING_USE_DOLLAR,
            label=f"Use "
            f"{Constants.TAG_PREFIX_SETTINGS[Constants.SETTING_USE_DOLLAR]}"
            f" tag prefix",
            field_type=Constants.FIELD_TYPE_BOOL,
            default=False,
            group=Constants.GROUP_CREATING,
            order=8,
        ),
        Setting(
            key=Constants.SETTING_USE_PLUS,
            label=f"Use "
            f"{Constants.TAG_PREFIX_SETTINGS[Constants.SETTING_USE_PLUS]}"
            f" tag prefix",
            field_type=Constants.FIELD_TYPE_BOOL,
            default=False,
            group=Constants.GROUP_CREATING,
            order=9,
        ),
        Setting(
            key=Constants.SETTING_USE_AMPERSAND,
            label=f"Use "
            f"{Constants.TAG_PREFIX_SETTINGS[Constants.SETTING_USE_AMPERSAND]}"
            f" tag prefix",
            field_type=Constants.FIELD_TYPE_BOOL,
            default=False,
            group=Constants.GROUP_CREATING,
            order=10,
        ),
        Setting(
            key=Constants.SETTING_USE_PERCENT,
            label=f"Use "
            f"{Constants.TAG_PREFIX_SETTINGS[Constants.SETTING_USE_PERCENT]}"
            f" tag prefix",
            field_type=Constants.FIELD_TYPE_BOOL,
            default=False,
            group=Constants.GROUP_CREATING,
            order=11,
        ),
        Setting(
            key=Constants.SETTING_USE_COLORS,
            label="Colored output",
            field_type=Constants.FIELD_TYPE_BOOL,
            default=True,
            group=Constants.GROUP_INTERFACE,
            order=1,
        ),
        Setting(
            key=Constants.SETTING_USE_CLEAR_SCREEN,
            label="Clear screen",
            field_type=Constants.FIELD_TYPE_BOOL,
            default=True,
            group=Constants.GROUP_INTERFACE,
            order=2,
        ),
        Setting(
            key=Constants.SETTING_USE_HINTS,
            label="Show hints",
            field_type=Constants.FIELD_TYPE_BOOL,
            default=True,
            group=Constants.GROUP_INTERFACE,
            order=3,
        ),
        Setting(
            key=Constants.SETTING_NOTES_PATH,
            label="Notes file path",
            field_type=Constants.FIELD_TYPE_STR,
            default=str(data_dir()),
            order=1,
            group=Constants.GROUP_SYSTEM,
        ),
        Setting(
            key=Constants.SETTING_LOG_LEVEL,
            label="Log level",
            field_type=Constants.FIELD_TYPE_CHOICE,
            default="low",
            group=Constants.GROUP_SYSTEM,
            order=2,
            options=list(Constants.LOG_LEVELS),
        ),
        Setting(
            key=Constants.SETTING_AUTO_SAVE,
            label="Autosave",
            field_type=Constants.FIELD_TYPE_BOOL,
            default=True,
            order=3,
            group=Constants.GROUP_SYSTEM,
        ),
    ]
