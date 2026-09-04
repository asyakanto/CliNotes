from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from app.constants import Constants
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

if TYPE_CHECKING:
    from collections.abc import Callable

    from app.app import NotesApp


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
    body += note.text or app.settings.get_str_value(Constants.SETTING_DEFAULT_TEXT)
    hints: str = (
        make_hint(
            f"Choose action: {Constants.KEY_QUIT} - quit;"
            f" {Constants.KEY_ARCHIVE} - archive note;"
            f" {Constants.KEY_EDIT} - edit note",
            style_config,
        )
        if not note.archived
        else make_hint(
            f"Choose action: {Constants.KEY_QUIT} - quit; "
            f"{Constants.KEY_RESTORE} - restore note;"
            f" {Constants.KEY_DELETE} - delete note",
            style_config,
        )
    )

    return build_view(header, body, hints)


def _format_deleting_at(note: Note, app: NotesApp) -> str:
    try:
        return get_date(
            datetime.strptime(
                note.archived_at,
                Constants.DATE_FORMAT_STORAGE,
            ).replace(tzinfo=get_local_now().tzinfo)
            + timedelta(
                days=app.settings.get_int_value(Constants.SETTING_AUTO_DELETE_DAYS)
            ),
            app.settings.date_pattern(),
        )
    except ValueError:
        return "unknown date"


def _resolve_edit(style_config: StyleConfig) -> Constants.ACTION_TYPE:

    editing_mode = prompt_input(
        hint=f"Edit: {Constants.KEY_EDIT_TITLE} "
        f"- title, {Constants.KEY_EDIT_TEXT} - text",
        style_config=style_config,
    )
    if editing_mode == Constants.KEY_EDIT_TITLE:
        return Constants.ACTION_CHANGE_TITLE
    if editing_mode == Constants.KEY_EDIT_TEXT:
        return Constants.ACTION_CHANGE_TEXT
    return Constants.ACTION_UNKNOWN


def note_interface(note: Note, style_config: StyleConfig) -> Constants.ACTION_TYPE:
    mode: str = read_input()
    if mode == Constants.KEY_QUIT:
        return Constants.ACTION_QUIT
    if note.archived:
        if mode == Constants.KEY_RESTORE:
            return Constants.ACTION_RESTORE
        if mode == Constants.KEY_DELETE:
            return Constants.ACTION_DELETE
    else:
        if mode == Constants.KEY_ARCHIVE:
            return Constants.ACTION_ARCHIVE
        if mode == Constants.KEY_EDIT:
            return _resolve_edit(style_config)
    return Constants.ACTION_UNKNOWN


def _archive_note(app: NotesApp, note: Note, style_config: StyleConfig) -> bool:
    if confirm(
        app=app,
        setting_key=Constants.SETTING_CONFIRM_ARCHIVE,
        message="Archive this note? (y/n)",
        danger=False,
        style_config=style_config,
    ):
        app.archive_note(note)
    return False


def _change_title(app: NotesApp, note: Note, style_config: StyleConfig) -> bool:
    new_title: str = prompt_input(
        hint="New title",
        prompt_default_text=note.title,
        lowercase=False,
        style_config=style_config,
    )
    app.edit_note(note, new_title, note.text)
    return False


def _change_text(app: NotesApp, note: Note, style_config: StyleConfig) -> bool:
    new_text: str = prompt_input(
        hint="New text",
        prompt_default_text=note.text,
        lowercase=False,
        style_config=style_config,
    )
    app.edit_note(note, note.title, new_text)
    return False


def _delete_note(app: NotesApp, note: Note, style_config: StyleConfig) -> bool:
    if confirm(
        app=app,
        setting_key=Constants.SETTING_CONFIRM_DELETE,
        message="Delete this note? (y/n)",
        danger=True,
        style_config=style_config,
    ):
        app.delete_note(note)
    return True


def _restore_note(app: NotesApp, note: Note) -> bool:
    app.restore_note(note)
    return False


def _unknown_action(style_config: StyleConfig) -> bool:
    pause("Wrong action", style_config)
    return False


def open_note(app: NotesApp, note: Note, style_config: StyleConfig) -> None:
    handlers: dict[Constants.ACTION_TYPE, Callable[[], bool]] = {
        Constants.ACTION_QUIT: lambda: True,
        Constants.ACTION_ARCHIVE: lambda: _archive_note(app, note, style_config),
        Constants.ACTION_CHANGE_TITLE: lambda: _change_title(app, note, style_config),
        Constants.ACTION_CHANGE_TEXT: lambda: _change_text(app, note, style_config),
        Constants.ACTION_RESTORE: lambda: _restore_note(app, note),
        Constants.ACTION_DELETE: lambda: _delete_note(app, note, style_config),
        Constants.ACTION_UNKNOWN: lambda: _unknown_action(style_config),
    }

    while True:
        clear_screen(style_config)
        print(show_note(note, app, style_config))  # noqa: T201
        action: Constants.ACTION_TYPE = note_interface(note, style_config)
        if handlers[action]():
            return
