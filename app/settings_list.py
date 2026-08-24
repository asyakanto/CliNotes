from pathlib import Path
from typing import Literal

from app.constants import Constants as C


class Setting:
    def __init__(
        self,
        key: str,
        label: str,
        field_type: Literal["int", "bool", "str", "choice"],
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
            (self.field_type == "bool" and isinstance(value, bool))
            or (
                self.field_type == "str"
                and isinstance(value, str)
                and (self.max_length is None or len(value) <= self.max_length)
            )
            or (
                self.field_type == "int"
                and not isinstance(value, bool)
                and isinstance(value, int)
                and (self.min_value is None or value >= self.min_value)
                and (self.max_value is None or value <= self.max_value)
            )
            or (
                self.field_type == "choice"
                and (value in self.options)
                and not isinstance(value, bool)
            )
        )


def build_default_settings() -> list[Setting]:
    return [
        Setting(
            key=C.SETTING_SHOW_ARCHIVED,
            label="Show archived notes",
            field_type="bool",
            default=False,
            group="display",
            order=1,
        ),
        Setting(
            key=C.DATE_FORMAT_SETTING,
            label="Date format",
            field_type="choice",
            default="DD-MM-YYYY",
            group="display",
            order=2,
            options=list(C.DATE_FORMAT_MAP.keys()),
        ),
        Setting(
            key=C.SETTING_AUTO_DELETE_DAYS,
            label="Days before auto deleting archived notes",
            field_type="int",
            default=30,
            group="archiving/deleting",
            order=1,
            min_value=1,
        ),
        Setting(
            key=C.SETTING_CONFIRM_ARCHIVE,
            label="Confirm before archiving note",
            field_type="bool",
            default=False,
            group="archiving/deleting",
            order=2,
        ),
        Setting(
            key=C.SETTING_CONFIRM_DELETE,
            label="Confirm before deleting note",
            field_type="bool",
            default=True,
            group="archiving/deleting",
            order=3,
        ),
        Setting(
            key=C.SETTING_AUTO_SYNC_TAGS,
            order=1,
            label="Auto-sync note tags",
            field_type="bool",
            default=True,
            group="creating a note",
        ),
        Setting(
            key=C.SETTING_AUTO_DATE_TAG,
            label="Add date tag to notes",
            field_type="bool",
            default=True,
            group="creating a note",
            order=2,
        ),
        Setting(
            key=C.SETTING_DEFAULT_TEXT,
            label="Default text for empty note",
            field_type="str",
            default="-",
            group="creating a note",
            order=3,
        ),
        Setting(
            key=C.SETTING_USE_AT,
            label=f"Use {C.TAG_PREFIX_SETTINGS[C.SETTING_USE_AT]} tag prefix",
            field_type="bool",
            default=True,
            group="creating a note",
            order=4,
        ),
        Setting(
            key=C.SETTING_USE_HASH,
            label=f"Use {C.TAG_PREFIX_SETTINGS[C.SETTING_USE_HASH]} tag prefix",
            field_type="bool",
            default=True,
            group="creating a note",
            order=5,
        ),
        Setting(
            key=C.SETTING_USE_TAG_COLON,
            label=f"Use {C.TAG_PREFIX_SETTINGS[C.SETTING_USE_TAG_COLON]} tag prefix",
            field_type="bool",
            default=True,
            group="creating a note",
            order=6,
        ),
        Setting(
            key=C.SETTING_USE_EXCLAMATION,
            label=f"Use {C.TAG_PREFIX_SETTINGS[C.SETTING_USE_EXCLAMATION]} tag prefix",
            field_type="bool",
            default=False,
            group="creating a note",
            order=7,
        ),
        Setting(
            key=C.SETTING_USE_DOLLAR,
            label=f"Use {C.TAG_PREFIX_SETTINGS[C.SETTING_USE_DOLLAR]} tag prefix",
            field_type="bool",
            default=False,
            group="creating a note",
            order=8,
        ),
        Setting(
            key=C.SETTING_USE_PLUS,
            label=f"Use {C.TAG_PREFIX_SETTINGS[C.SETTING_USE_PLUS]} tag prefix",
            field_type="bool",
            default=False,
            group="creating a note",
            order=9,
        ),
        Setting(
            key=C.SETTING_USE_AMPERSAND,
            label=f"Use {C.TAG_PREFIX_SETTINGS[C.SETTING_USE_AMPERSAND]} tag prefix",
            field_type="bool",
            default=False,
            group="creating a note",
            order=10,
        ),
        Setting(
            key=C.SETTING_USE_PERCENT,
            label=f"Use {C.TAG_PREFIX_SETTINGS[C.SETTING_USE_PERCENT]} tag prefix",
            field_type="bool",
            default=False,
            group="creating a note",
            order=11,
        ),
        Setting(
            key=C.SETTING_USE_COLORS,
            label="Colored output",
            field_type="bool",
            default=True,
            group="interface",
            order=1,
        ),
        Setting(
            key=C.SETTING_USE_CLEAR_SCREEN,
            label="Clear screen",
            field_type="bool",
            default=True,
            group="interface",
            order=2,
        ),
        Setting(
            key=C.SETTING_USE_HINTS,
            label="Show hints",
            field_type="bool",
            default=True,
            group="interface",
            order=3,
        ),
        Setting(
            key=C.SETTING_NOTES_PATH,
            label="Notes file path",
            field_type="str",
            default=str(Path(__file__).parent.parent),
            order=1,
            group="system",
        ),
        Setting(
            key=C.SETTING_LOG_LEVEL,
            label="Log level",
            field_type="choice",
            default="low",
            group="system",
            order=2,
            options=list(C.LOG_LEVELS),
        ),
        Setting(
            key=C.SETTING_AUTO_SAVE,
            label="Autosave",
            field_type="bool",
            default=True,
            order=3,
            group="system",
        ),
    ]
