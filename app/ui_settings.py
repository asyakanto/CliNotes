from app.app import NotesApp
from app.constants import Constants as C
from app.settings_list import Setting
from app.ui_input import pause, prompt_input, read_input
from app.ui_style import (
    StyleConfig,
    apply_settings,
    build_view,
    clear_screen,
    get_header,
    make_cyan,
    make_hint,
)


def show_settings_categories(app: NotesApp, style_config: StyleConfig) -> str:
    header: str = get_header("Settings", style_config)
    hints: str = make_hint(
        "Actions: {ID} - open category; "
        f"{C.KEY_PERCENT_QUIT} - quit; {C.KEY_RESET_SETTINGS} - reset all settings",
        style_config,
    )
    lines: list[str] = []
    for i, group in enumerate(app.settings.groups()):
        lines.append(f"{i} - {group}")
    body: str = "\n".join(lines)

    return build_view(header, body, hints)


def settings_interface(app: NotesApp, style_config: StyleConfig) -> None:
    groups = app.settings.groups()
    while True:
        clear_screen(style_config)
        print(show_settings_categories(app, style_config))
        action: str = read_input()
        if action == C.KEY_PERCENT_QUIT:
            return
        if action == C.KEY_RESET_SETTINGS:
            if (
                prompt_input(
                    "Reset all settings? (y/n)",
                    lowercase=True,
                    danger=True,
                    style_config=style_config,
                )
                == "y"
            ):
                app.reset_settings()
                apply_settings(app, style_config)
                app.add_notification("Settings reset to defaults")
        elif action.isdigit():
            if 0 <= int(action) < len(groups):
                settings_group_interface(app, groups[int(action)], style_config)
            else:
                pause("Wrong ID", style_config)

        else:
            pause("Wrong action", style_config)


def show_settings_group(
    app: NotesApp,
    group_name: str,
    group_settings: list[Setting],
    style_config: StyleConfig,
) -> str:
    header: str = get_header(group_name, style_config)
    lines: list[str] = []
    for i, setting in enumerate(group_settings):
        if isinstance(setting.value, bool):
            value: str = "on" if setting.value else "off"

        else:
            value = str(setting.value)
        lines.append(
            str(i) + " - " + setting.label + " - " + make_cyan(value, style_config)
        )
    body: str = "\n".join(lines)
    hints: str = make_hint(
        "Actions: {ID} - change setting; " + f"{C.KEY_PERCENT_QUIT} - quit",
        style_config,
    )

    return build_view(header, body, hints)


def settings_group_interface(
    app: NotesApp, group: str, style_config: StyleConfig
) -> None:
    group_settings: list[Setting] = app.settings.settings_in_group(group)
    while True:
        clear_screen(style_config)
        print(show_settings_group(app, group, group_settings, style_config))
        action: str = read_input()
        if action == C.KEY_PERCENT_QUIT:
            app.save_settings()
            return
        if action.isdigit():
            if 0 <= int(action) < len(group_settings):
                edit_setting(app, group_settings[int(action)], style_config)
            else:
                pause("Wrong ID", style_config)

        else:
            pause("Wrong action", style_config)


def edit_setting(app: NotesApp, setting: Setting, style_config: StyleConfig) -> None:
    match setting.field_type:
        case C.FIELD_TYPE_BOOL:
            _edit_bool_setting(app, setting, style_config)
        case C.FIELD_TYPE_INT:
            _edit_int_setting(app, setting, style_config)
        case C.FIELD_TYPE_STR:
            _edit_str_setting(app, setting, style_config)
        case C.FIELD_TYPE_CHOICE:
            _edit_choice_setting(app, setting, style_config)


def _edit_bool_setting(
    app: NotesApp, setting: Setting, style_config: StyleConfig
) -> None:
    app.settings.set_value(setting.key, not app.settings.get_bool_value(setting.key))
    apply_settings(app, style_config, setting.key)


def _edit_str_setting(
    app: NotesApp, setting: Setting, style_config: StyleConfig
) -> None:
    max_length: int | None = setting.max_length
    if max_length is not None:
        clue = f"Enter a text (max length is {max_length} characters)"
    else:
        clue = "Enter a text"
    value = prompt_input(hint=clue, lowercase=False, style_config=style_config)
    if value == C.KEY_PERCENT_QUIT:
        return
    edited_str: bool = app.settings.set_value(setting.key, value)
    if edited_str:
        apply_settings(app, style_config, setting.key)

    else:
        pause(f"Text length is over than {max_length} characters", style_config)


def _edit_int_setting(
    app: NotesApp, setting: Setting, style_config: StyleConfig
) -> None:
    clue: str = ""
    min_value: int | None = setting.min_value
    max_value: int | None = setting.max_value
    if min_value is None and max_value is None:
        clue = "Enter any number"
    else:
        clue += "Range: " + _range_clue(min_value, max_value)
    value = prompt_input(hint=clue, lowercase=False, style_config=style_config)
    if value == C.KEY_PERCENT_QUIT:
        return
    if value.isdigit():
        edited: bool = app.settings.set_value(setting.key, int(value))
        if edited:
            apply_settings(app, style_config, setting.key)

        else:
            pause(
                f"number is not in range {_range_clue(min_value, max_value)}",
                style_config,
            )
    else:
        pause("not a number", style_config)


def _edit_choice_setting(
    app: NotesApp, setting: Setting, style_config: StyleConfig
) -> None:
    choices: list[str | int] = setting.options
    _render_choice_page(setting, choices, style_config)
    value: str = read_input(lowercase=False)
    if value == C.KEY_PERCENT_QUIT:
        return
    if value.isdigit() and 0 <= int(value) < len(choices):
        app.settings.set_value(setting.key, choices[int(value)])
        apply_settings(app, style_config, setting.key)
    else:
        pause("Wrong ID", style_config)


def _range_clue(min: int | None = None, max: int | None = None) -> str:
    clue = ""
    if min is not None:
        clue += str(min)
    clue += ".."
    if max is not None:
        clue += str(max)

    return clue


def _render_choice_page(
    setting: Setting, choices: list[str | int], style_config: StyleConfig
) -> None:
    clear_screen(style_config)
    lines: list[str] = []
    for i, choice in enumerate(choices):
        lines.append(f"{i} {choice}")
    body: str = "\n".join(lines)
    header: str = get_header(setting.label, style_config)
    hints: str = make_hint("choose option ID", style_config)
    print(build_view(header, body, hints))
