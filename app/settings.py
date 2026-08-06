from typing import Literal


class Settings:
    def __init__(self) -> None:
        self._items: dict[str, Setting] = {
            "show_archived_notes": Setting(
                label="Show archived notes",
                field_type="bool",
                default=False,
                group="display",
                order=1,
            ),
            "separator_width": Setting(
                label="Separator width",
                field_type="int",
                default=15,
                group="display",
                order=2,
                min_value=5,
                max_value=40,
            ),
            "date_format": Setting(
                label="Date format",
                field_type="choice",
                default="DD-MM-YYYY",
                group="display",
                order=3,
                options=["DD-MM-YYYY", "DD.MM.YYYY", "YYYY-MM-DD", "DD/MM/YYYY"],
            ),
        }

    def get_value(self, setting_name: str) -> int | str | None | bool:
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


class Setting:
    def __init__(
        self,
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
                and (
                    self.max_length is None
                    or type(value) == "str"
                    and len(value) <= self.max_length
                )
            )
            or (
                self.field_type == "int"
                and (
                    self.min_value is None
                    or type(value) == "int"
                    and value >= self.min_value
                )
                and (
                    self.max_value is None
                    or type(value) == "int"
                    and value <= self.max_value
                )
            )
            or (self.field_type == "choice" and (value in self.options))
        )
