import logging
from typing import Any

from app.constants import Constants as C
from app.models import get_date_format
from app.settings_list import Setting, build_default_settings

logger = logging.getLogger(__name__)


class Settings:
    def __init__(self) -> None:
        self._config: dict[str, Setting] = {s.key: s for s in build_default_settings()}

    def _get_value(self, key: str) -> int | bool | str | None:
        setting: Setting | None = self._config.get(key)
        if setting is None:
            raise KeyError(f"Settings key '{key}' not found in configuration")
        return setting.value

    def get_bool_value(self, key: str) -> bool:
        value = self._get_value(key)
        if isinstance(value, bool):
            return value
        raise TypeError(
            f"Setting '{key}' has type {type(value).__name__}, expected bool"
        )

    def get_int_value(self, key: str) -> int:
        value = self._get_value(key)
        if isinstance(value, int) and not isinstance(value, bool):
            return value
        raise TypeError(
            f"Setting '{key}' has type {type(value).__name__}, expected int"
        )

    def get_str_value(self, key: str) -> str:
        value = self._get_value(key)
        if isinstance(value, str):
            return value
        raise TypeError(
            f"Setting '{key}' has type {type(value).__name__}, expected str"
        )

    def set_value(self, key: str, value: bool | str | int) -> bool:
        setting: Setting | None = self._config.get(key)
        if setting is None:
            raise KeyError(f"Settings key '{key}' not found in configuration")
        if setting.validate(value):
            setting.value = value
            return True
        return False

    def settings_to_dict(self) -> dict[str, Any]:
        return {setting.key: setting.value for setting in self._config.values()}

    def dict_to_settings(self, settings_dict: dict[str, Any]) -> None:
        for key, value in settings_dict.items():
            setting: Setting | None = self._config.get(key)
            if setting is None:
                logger.warning(f"Unknown setting key '{key}' ignored")
                continue
            if setting.validate(value):
                setting.value = value
            else:
                logger.warning(f"Invalid value '{value}' for setting '{key}' ")

    def date_pattern(self) -> str:
        value: str = self.get_str_value(C.DATE_FORMAT_SETTING)
        return get_date_format(value)

    def groups(self) -> list[str]:
        groups: list[str] = list(dict.fromkeys(x.group for x in self._config.values()))
        return groups

    def settings_in_group(self, group: str) -> list[Setting]:
        settings: list[Setting] = [x for x in self._config.values() if x.group == group]
        settings = sorted(settings, key=lambda x: x.order)
        return settings

    def active_tag_prefixes(self) -> list[str]:
        active_tags: list[str] = []
        for key, tag in C.TAG_PREFIX_SETTINGS.items():
            if self.get_bool_value(key):
                active_tags.append(tag)
        return active_tags

    def reset_all(self) -> None:
        for setting in self._config.values():
            setting.value = setting.default

    def reset_setting(self, key: str) -> None:
        setting: Setting | None = self._config.get(key)
        if setting is None:
            raise KeyError(f"Settings key '{key}' not found in configuration")
        self.set_value(key, setting.default)
