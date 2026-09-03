from app.app import NotesApp
from app.constants import Constants as C
from app.models import Note, get_date, get_local_now, get_plural
from app.ui_input import read_input
from app.ui_style import (
    StyleConfig,
    build_view,
    clear_screen,
    get_header,
    make_hint,
    make_muted,
    make_red,
)


def get_visible_notes(notes: list[Note], display_archive: bool) -> list[Note]:
    if display_archive:
        return notes
    notes_list: list[Note] = []
    for note in notes:
        if not note.archived:
            notes_list.append(note)

    return notes_list


def display_notes(notes: list[Note], style_config: StyleConfig) -> str:
    if len(notes) != 0:
        lines: list[str] = []
        for note in notes:
            if not note.archived:
                lines.append(f"#{note.id} {note.title}")
            else:
                lines.append(make_muted(f"#{note.id} {note.title}", style_config))
        return "\n".join(lines)
    return make_muted(f"No notes yet — press {C.KEY_CREATE} to create", style_config)


def get_notifications(app: NotesApp, style_config: StyleConfig) -> str:

    lines: list[str] = []
    for notification in app.pop_notifications():
        lines.append(make_red("[!] " + notification, style_config))
    return "\n".join(lines)


def show_main_menu(app: NotesApp, style_config: StyleConfig) -> str:
    visible_notes: list[Note] = get_visible_notes(
        app.notes, app.settings.get_bool_value(C.SETTING_SHOW_ARCHIVED)
    )
    header: str = get_header(
        f"CliNotes: {get_date(get_local_now(), app.settings.date_pattern())} "
        f"· {get_plural(len(visible_notes), 'note')}",
        style_config,
    )
    body: str = "\n\n".join(
        section
        for section in [
            get_notifications(app, style_config),
            display_notes(visible_notes, style_config),
        ]
        if section
    )

    hints: str = make_hint(
        "Actions: {ID}"
        f" - open note; {C.KEY_QUIT} - quit; {C.KEY_CREATE} - create; "
        f"{C.KEY_SEARCH} - search; {C.KEY_TOGGLE_ARCHIVED} - show archived; "
        f"{C.KEY_SETTINGS} - settings",
        style_config,
    )

    return build_view(header, body, hints)


def display_main_menu(app: NotesApp, style_config: StyleConfig) -> str:
    clear_screen(style_config)
    print(show_main_menu(app, style_config))
    return read_input()
