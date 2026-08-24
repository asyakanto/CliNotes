from app.app import NotesApp
from app.constants import Constants as C
from app.models import Note, get_date, get_local_now
from app.ui_input import read_input
from app.ui_style import (
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


def display_notes(notes: list[Note]) -> str:
    if len(notes) != 0:
        lines: list[str] = []
        for note in notes:
            if not note.archived:
                lines.append(f"#{note.id} {note.title}")
            else:
                lines.append(make_muted(f"#{note.id} {note.title}"))
        return "\n".join(lines)
    return make_muted(f"No notes yet — press {C.KEY_CREATE} to create")


def get_notifications(app: NotesApp) -> str:
    if not app._notifications:
        return ""

    lines: list[str] = []
    for notification in app.pop_notifications():
        lines.append(make_red("[!] " + notification))
    return "\n".join(lines)


def show_main_menu(app: NotesApp) -> str:
    visible_notes: list[Note] = get_visible_notes(
        app.notes, app.settings.get_bool_value(C.SETTING_SHOW_ARCHIVED)
    )
    header: str = get_header(
        f"CliNotes: {get_date(get_local_now(), app.settings.date_pattern())} · {len(visible_notes)} {'notes' if len(visible_notes) != 1 and len(visible_notes) != 0 else 'note'}"
    )
    body: str = "\n\n".join(
        section
        for section in [get_notifications(app), display_notes(visible_notes)]
        if section
    )

    hints: str = make_hint(
        "Actions: {ID}"
        + f" - open note; {C.KEY_QUIT} - quit; {C.KEY_CREATE} - create; {C.KEY_SEARCH} - search; {C.KEY_TOGGLE_ARCHIVED} - show archived; {C.KEY_SETTINGS} - settings"
    )

    return build_view(header, body, hints)


def main_interface() -> str:

    mode = read_input()

    return mode


def display_main_menu(app: NotesApp) -> str:
    clear_screen()
    print(show_main_menu(app))
    mode: str = main_interface()
    return mode
