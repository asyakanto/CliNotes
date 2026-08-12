from typing import Any, Literal

from app.constants import (
    DATE_FORMAT_MAP,
    DATE_FORMAT_SETTING,
    DATE_FORMAT_STORAGE,
    DEFAULT_SEPARATOR_WIDTH,
    SEPARATOR_WIDTH,
    SETTING_SHOW_ARCHIVED,
)
from app.models import get_date_format


class Settings:
    def __init__(self) -> None:
        definition: list[Setting] = [
            Setting(
                key=SETTING_SHOW_ARCHIVED,
                label="Show archived notes",
                field_type="bool",
                default=False,
                group="display",
                order=1,
            ),
            Setting(
                key=SEPARATOR_WIDTH,
                label="Separator width",
                field_type="int",
                default=DEFAULT_SEPARATOR_WIDTH,
                group="display",
                order=2,
                min_value=5,
                max_value=40,
            ),
            Setting(
                key=DATE_FORMAT_SETTING,
                label="Date format",
                field_type="choice",
                default="DD-MM-YYYY",
                group="display",
                order=3,
                options=list(DATE_FORMAT_MAP.keys()),
            ),
        ]
        self._items: dict[str, Setting] = {s.key: s for s in definition}

    def get_value(self, setting_name: str) -> int | str | bool | None:
        if setting_name in self._items:
            setting: Setting | None = self._items.get(setting_name)
            if setting:
                return setting.value if setting.value is not None else setting.default
        return None

    def set_value(self, setting_name: str, value: bool | str | int) -> bool:
        if setting_name in self._items:
            setting: Setting | None = self._items.get(setting_name)
            if setting and setting.validate(value):
                setting.value = value
                return True
        return False

    def settings_to_dict(self) -> dict[str, Any]:
        settings_dict: dict[str, Any] = {}
        for key, item in self._items.items():
            settings_dict.update({key: item.value})
        return settings_dict

    def dict_to_settings(self, settings_dict: dict[str, Any]) -> None:
        for key, value in settings_dict.items():
            try:
                if self._items[key].validate(value):
                    self._items[key].value = value
            except KeyError:
                continue

    def date_pattern(self) -> str:
        value: int | str | None = self.get_value(DATE_FORMAT_SETTING)
        if not isinstance(value, str):
            value = DATE_FORMAT_STORAGE
        return get_date_format(value)

    def groups(self) -> list[str]:
        groups: list[str] = list(dict.fromkeys(x.group for x in self._items.values()))
        return groups

    def settings_in_group(self, group: str) -> list[Setting]:
        settings: list[Setting] = [x for x in self._items.values() if x.group == group]
        settings = sorted(settings, key=lambda x: x.order)
        return settings


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
            (self.field_type == "bool" and (value is False or value is True))
            or (
                self.field_type == "str"
                and type(value) == str
                and (self.max_length is None or len(value) <= self.max_length)
            )
            or (
                self.field_type == "int"
                and type(value) == int
                and (self.min_value is None or value >= self.min_value)
                and (self.max_value is None or value <= self.max_value)
            )
            or (self.field_type == "choice" and (value in self.options))
        )
