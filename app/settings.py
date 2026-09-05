"""Settings access layer for the CliNotes application."""

import logging
from typing import Any

from app.constants import Constants
from app.models import get_date_format
from app.settings_list import Setting, build_default_settings

logger = logging.getLogger(__name__)


class Settings:
    """Store and provide typed access to application settings."""

    def __init__(self) -> None:
        """Build the config map from default settings."""
        self._config: dict[str, Setting] = {s.key: s for s in build_default_settings()}

    def _get_value(self, key: str) -> int | bool | str | None:
        setting: Setting | None
        if (setting := self._config.get(key)) is None:
            raise KeyError(Constants.SETTINGS_KEY_NOT_FOUND % key)
        return setting.value

    def get_bool_value(self, key: str) -> bool:
        """Return the setting value as bool."""
        value = self._get_value(key)
        if isinstance(value, bool):
            return value
        raise TypeError(
            Constants.SETTINGS_TYPE_MISMATCH % (key, type(value).__name__, "bool")
        )

    def get_int_value(self, key: str) -> int:
        """Return the setting value as int."""
        value = self._get_value(key)
        if isinstance(value, int) and not isinstance(value, bool):
            return value
        raise TypeError(
            Constants.SETTINGS_TYPE_MISMATCH % (key, type(value).__name__, "int")
        )

    def get_str_value(self, key: str) -> str:
        """Return the setting value as str."""
        value = self._get_value(key)
        if isinstance(value, str):
            return value
        raise TypeError(
            Constants.SETTINGS_TYPE_MISMATCH % (key, type(value).__name__, "str")
        )

    def set_value(self, key: str, value: bool | str | int) -> bool:  # noqa: FBT001
        """Set a setting value if it validates."""
        setting: Setting | None
        if (setting := self._config.get(key)) is None:
            raise KeyError(Constants.SETTINGS_KEY_NOT_FOUND % key)
        if setting.validate(value):
            setting.value = value
            return True
        return False

    def settings_to_dict(self) -> dict[str, Any]:
        """Return all settings as a key-value mapping."""
        return {setting.key: setting.value for setting in self._config.values()}

    def dict_to_settings(self, settings_dict: dict[str, Any]) -> None:
        """Apply a key-value mapping to settings."""
        for key, value in settings_dict.items():
            setting: Setting | None
            if (setting := self._config.get(key)) is None:
                logger.warning("Unknown setting key '%s' ignored", key)
                continue
            if setting.validate(value):
                setting.value = value
            else:
                logger.warning("Invalid value '%s' for setting '%s' ", value, key)

    def date_pattern(self) -> str:
        """Return the configured date pattern for display."""
        value: str = self.get_str_value(Constants.DATE_FORMAT_SETTING)
        return get_date_format(value)

    def groups(self) -> list[str]:
        """Return the unique setting groups."""
        groups: list[str] = list(dict.fromkeys(x.group for x in self._config.values()))
        return groups

    def settings_in_group(self, group: str) -> list[Setting]:
        """Return settings of a group, ordered."""
        return sorted(
            [x for x in self._config.values() if x.group == group],
            key=lambda x: x.order,
        )

    def active_tag_prefixes(self) -> list[str]:
        """Return the active tag prefixes."""
        active_tags: list[str] = []
        for key, tag in Constants.TAG_PREFIX_SETTINGS.items():
            if self.get_bool_value(key):
                active_tags.append(tag)
        return active_tags

    def reset_all(self) -> None:
        """Reset all settings to defaults."""
        for setting in self._config.values():
            setting.value = setting.default

    def reset_setting(self, key: str) -> None:
        """Reset a single setting to its default."""
        setting: Setting | None
        if (setting := self._config.get(key)) is None:
            raise KeyError(Constants.SETTINGS_KEY_NOT_FOUND % key)
        self.set_value(key, setting.default)
