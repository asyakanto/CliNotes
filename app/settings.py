from typing import Any, Literal

from app.constants import Constants as C
from app.models import get_date_format
from app.settings_list import build_default_settings


class Settings:
    def __init__(self) -> None:
        self._items: dict[str, Setting] = {s.key: s for s in build_default_settings()}

    def get_value(self, setting_name: str) -> int | str | bool | None:
        if setting_name in self._items:
            setting: Setting | None = self._items.get(setting_name)
            if setting:
                return setting.value if setting.value is not None else setting.default
        return None

    def get_bool_value(self, setting_name: str) -> bool:
        value = self.get_value(setting_name)
        if isinstance(value, bool):
            return value
        setting = self._items.get(setting_name)
        if setting is not None and isinstance(setting.default, bool):
            return setting.default
        return True

    def get_int_value(self, setting_name: str) -> int:
        value = self.get_value(setting_name)
        if isinstance(value, int):
            return value
        setting = self._items.get(setting_name)
        if setting is not None and isinstance(setting.default, int):
            return setting.default
        return 1

    def get_str_value(self, setting_name: str) -> str:
        value = self.get_value(setting_name)
        if isinstance(value, str):
            return value
        setting = self._items.get(setting_name)
        if setting is not None and isinstance(setting.default, str):
            return setting.default
        return ""

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
        value: int | str | None = self.get_value(C.DATE_FORMAT_SETTING)
        if not isinstance(value, str):
            value = C.DATE_FORMAT_STORAGE
        return get_date_format(value)

    def groups(self) -> list[str]:
        groups: list[str] = list(dict.fromkeys(x.group for x in self._items.values()))
        return groups

    def settings_in_group(self, group: str) -> list[Setting]:
        settings: list[Setting] = [x for x in self._items.values() if x.group == group]
        settings = sorted(settings, key=lambda x: x.order)
        return settings

    def active_tag_prefixes(self) -> list[str]:
        active_tags: list[str] = []
        for key, tag in C.TAG_PREFIX_SETTINGS.items():
            if self.get_bool_value(key):
                active_tags.append(tag)
        return active_tags

    def reset_all(self) -> None:
        for setting in self._items.values():
            setting.value = setting.default

    def reset_setting(self, key: str) -> None:
        self.set_value(key, self._items[key].default)


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
