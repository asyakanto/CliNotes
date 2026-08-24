from app.app import NotesApp
from app.constants import Constants as C
from app.settings import Setting
from app.ui_input import pause, prompt_input, read_input
from app.ui_style import (
    build_view,
    clear_screen,
    get_header,
    make_cyan,
    make_hint,
    set_clear_screen_enabled,
    set_colors_enabled,
    set_hints_enabled,
)


def show_settings_categories(app: NotesApp) -> str:
    header: str = get_header("Settings")
    hints: str = make_hint(
        "Actions: {ID} - open category; "
        + f"{C.KEY_SEARCH_QUIT} - quit; {C.KEY_RESET_SETTINGS} - reset all settings"
    )
    lines: list[str] = []
    for i, group in enumerate(app.settings.groups()):
        lines.append(f"{i} - {group}")
    body: str = "\n".join(lines)

    return build_view(header, body, hints)


def settings_interface(app: NotesApp) -> None:
    groups = app.settings.groups()
    while True:
        clear_screen()
        print(show_settings_categories(app))
        action: str = read_input()
        if action == C.KEY_SEARCH_QUIT:
            return
        elif action == C.KEY_RESET_SETTINGS:
            if (
                prompt_input("Reset all settings? (y/n)", lowercase=True, danger=True)
                == "y"
            ):
                app.reset_settings()
                set_colors_enabled(app.settings.get_bool_value(C.SETTING_USE_COLORS))
                set_clear_screen_enabled(
                    app.settings.get_bool_value(C.SETTING_USE_CLEAR_SCREEN)
                )
                set_hints_enabled(app.settings.get_bool_value(C.SETTING_USE_HINTS))
                app.sync_tags_if_enabled()
                app.apply_log_level()
                app.apply_notes_path()
                app.add_notification("Settings reset to defaults")
        elif action.isdigit() and "." not in action:
            if 0 <= int(action) < len(groups):
                settings_group_interface(app, groups[int(action)])
            else:
                pause("Wrong ID")

        else:
            pause("Wrong action")


def show_settings_group(
    app: NotesApp, group_name: str, group_settings: list[Setting]
) -> str:
    header: str = get_header(group_name)
    lines: list[str] = []
    for i, setting in enumerate(group_settings):
        value: str = ""
        if type(setting.value) == bool:
            if setting.value:
                value = "on"
            else:
                value = "off"
        else:
            value = str(setting.value)
        lines.append(str(i) + " - " + setting.label + " - " + make_cyan(value))
    body: str = "\n".join(lines)
    hints: str = make_hint(
        "Actions: {ID} - change setting; " + f"{C.KEY_SEARCH_QUIT} - quit"
    )

    return build_view(header, body, hints)


def settings_group_interface(app: NotesApp, group: str) -> None:
    group_settings: list[Setting] = app.settings.settings_in_group(group)
    while True:
        clear_screen()
        print(show_settings_group(app, group, group_settings))
        action: str = read_input()
        if action == C.KEY_SEARCH_QUIT:
            app.save_settings()
            return
        elif action.isdigit() and "." not in action:
            if 0 <= int(action) < len(group_settings):
                edit_setting(app, group_settings[int(action)])
            else:
                pause("Wrong ID")

        else:
            pause("Wrong action")


def edit_setting(app: NotesApp, setting: Setting) -> None:
    match setting.field_type:
        case "bool":
            _edit_bool_setting(app, setting)
        case "int":
            _edit_int_setting(app, setting)
        case "str":
            _edit_str_setting(app, setting)
        case "choice":
            _edit_choice_setting(app, setting)


def _edit_bool_setting(app: NotesApp, setting: Setting) -> None:
    app.settings.set_value(setting.key, not app.settings.get_bool_value(setting.key))
    if setting.key == C.SETTING_USE_COLORS:
        set_colors_enabled(app.settings.get_bool_value(C.SETTING_USE_COLORS))
    if setting.key == C.SETTING_USE_CLEAR_SCREEN:
        set_clear_screen_enabled(
            app.settings.get_bool_value(C.SETTING_USE_CLEAR_SCREEN)
        )
    if setting.key == C.SETTING_USE_HINTS:
        set_hints_enabled(app.settings.get_bool_value(C.SETTING_USE_HINTS))
    if (
        setting.key in C.TAG_PREFIX_SETTINGS
        or setting.key == C.SETTING_AUTO_DATE_TAG
        or setting.key == C.SETTING_AUTO_SYNC_TAGS
    ):
        app.sync_tags_if_enabled()


def _edit_str_setting(app: NotesApp, setting: Setting) -> None:
    max_length: int | None = setting.max_length
    if max_length is not None:
        clue = f"Enter a text (max length is {max_length} characters)"
    else:
        clue = "Enter a text"
    value = prompt_input(hint=clue, lowercase=False)
    if value == "%q":
        return
    edited_str: bool = app.settings.set_value(setting.key, value)
    if not edited_str:
        pause(f"Text length is over than {max_length} characters")

    if setting.key == C.SETTING_NOTES_PATH:
        app.apply_notes_path()


def _edit_int_setting(app: NotesApp, setting: Setting) -> None:
    clue: str = ""
    min_value: int | None = setting.min_value
    max_value: int | None = setting.max_value
    if min_value is None and max_value is None:
        clue = "Enter any number"
    else:
        clue += "Range: " + _range_clue(min_value, max_value)
    value = prompt_input(hint=clue, lowercase=False)
    if value == "%q":
        return
    elif value.isdigit() and "." not in value:
        edited: bool = app.settings.set_value(setting.key, int(value))
        if not edited:
            pause(f"number is not in range {_range_clue(min_value, max_value)}")
    else:
        pause("not a number")


def _edit_choice_setting(app: NotesApp, setting: Setting) -> None:
    choices: list[str | int] = [choice for choice in setting.options]
    _render_choice_page(setting, choices)
    value: str = read_input(lowercase=False)
    if value == "%q":
        return
    elif value.isdigit() and "." not in value and 0 <= int(value) < len(choices):
        app.settings.set_value(setting.key, choices[int(value)])
        if setting.key == C.SETTING_LOG_LEVEL:
            app.apply_log_level()
    else:
        pause("Wrong ID")


def _range_clue(min: int | None = None, max: int | None = None) -> str:
    clue = ""
    if min is not None:
        clue += str(min)
    clue += ".."
    if max is not None:
        clue += str(max)

    return clue


def _render_choice_page(setting: Setting, choices: list[str | int]) -> None:
    clear_screen()
    lines: list[str] = []
    for i, choice in enumerate(choices):
        lines.append(f"{i} {choice}")
    body: str = "\n".join(lines)
    header: str = get_header(setting.label)
    hints: str = make_hint("choose option ID")
    print(build_view(header, body, hints))
