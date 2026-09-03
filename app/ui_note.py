from datetime import datetime, timedelta

from app.app import NotesApp
from app.constants import Constants as C
from app.models import Note, get_date, get_local_now, has_easter_egg
from app.ui_input import confirm, pause, prompt_input, read_input
from app.ui_style import (
    StyleConfig,
    build_view,
    clear_screen,
    get_header,
    make_hint,
    make_muted,
    make_red,
)


def show_note(note: Note, app: NotesApp, style_config: StyleConfig) -> str:
    header: str = get_header(note.title, style_config, pink=has_easter_egg(note.text))
    body: str = ""
    if note.archived:
        deleting_at: str = _format_deleting_at(note, app)
        body += make_red(
            f"ARCHIVED: note will be deleted at {deleting_at}\n", style_config
        )
    body += make_muted(
        str(note.id) + " #: " + ", ".join(note.tags) + "\n\n", style_config
    )
    body += (
        note.text or app.settings.get_str_value(C.SETTING_DEFAULT_TEXT)
    )
    hints: str = (
        make_hint(
            f"Choose action: {C.KEY_QUIT} - quit; {C.KEY_ARCHIVE} - archive note; {C.KEY_EDIT} - edit note",
            style_config,
        )
        if not note.archived
        else make_hint(
            f"Choose action: {C.KEY_QUIT} - quit; {C.KEY_RESTORE} - restore note; {C.KEY_DELETE} - delete note",
            style_config,
        )
    )

    return build_view(header, body, hints)


def _format_deleting_at(note: Note, app: NotesApp) -> str:
    try:
        return get_date(
            datetime.strptime(
                note.archived_at,
                C.DATE_FORMAT_STORAGE,
            ).replace(tzinfo=get_local_now().tzinfo)
            + timedelta(days=app.settings.get_int_value(C.SETTING_AUTO_DELETE_DAYS)),
            app.settings.date_pattern(),
        )
    except ValueError:
        return "unknown date"


def note_interface(note: Note, style_config: StyleConfig) -> C.ACTION_TYPE:
    mode: str
    mode = read_input()
    if not note.archived:
        match mode:
            case C.KEY_QUIT:
                return C.ACTION_QUIT
            case C.KEY_ARCHIVE:
                return C.ACTION_ARCHIVE
            case C.KEY_EDIT:
                editing_mode: str = prompt_input(
                    hint=f"Edit: {C.KEY_EDIT_TITLE} - title, {C.KEY_EDIT_TEXT} - text",
                    style_config=style_config,
                )
                if editing_mode == C.KEY_EDIT_TITLE:
                    return C.ACTION_CHANGE_TITLE
                if editing_mode == C.KEY_EDIT_TEXT:
                    return C.ACTION_CHANGE_TEXT

    else:
        match mode:
            case C.KEY_QUIT:
                return C.ACTION_QUIT
            case C.KEY_RESTORE:
                return C.ACTION_RESTORE
            case C.KEY_DELETE:
                return C.ACTION_DELETE
    return C.ACTION_UNKNOWN


def open_note(app: NotesApp, note: Note, style_config: StyleConfig) -> None:
    while True:
        clear_screen(style_config)
        print(show_note(note, app, style_config))
        action: C.ACTION_TYPE = note_interface(note, style_config)

        match action:
            case C.ACTION_QUIT:
                break
            case C.ACTION_ARCHIVE:
                if confirm(
                    app=app,
                    setting_key=C.SETTING_CONFIRM_ARCHIVE,
                    message="Archive this note? (y/n)",
                    danger=False,
                    style_config=style_config,
                ):
                    app.archive_note(note)
            case C.ACTION_CHANGE_TITLE:
                new_title: str = prompt_input(
                    hint="New title",
                    prompt_default_text=note.title,
                    lowercase=False,
                    style_config=style_config,
                )
                app.edit_note(note, new_title, note.text)
            case C.ACTION_CHANGE_TEXT:
                new_text: str = prompt_input(
                    hint="New text",
                    prompt_default_text=note.text,
                    lowercase=False,
                    style_config=style_config,
                )
                app.edit_note(note, note.title, new_text)
            case C.ACTION_UNKNOWN:
                pause("Wrong action", style_config)
            case C.ACTION_RESTORE:
                app.restore_note(note)
            case C.ACTION_DELETE:
                if confirm(
                    app=app,
                    setting_key=C.SETTING_CONFIRM_DELETE,
                    message="Delete this note? (y/n)",
                    danger=True,
                    style_config=style_config,
                ):
                    app.delete_note(note)
                    break
