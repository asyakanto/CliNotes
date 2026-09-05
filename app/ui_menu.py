"""Rendering of the main menu and note lists."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.constants import Constants
from app.models import get_date, get_local_now, get_plural
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

if TYPE_CHECKING:
    from app.app import NotesApp
    from app.models import Note


def get_visible_notes(notes: list[Note], *, display_archive: bool) -> list[Note]:
    """Return notes, respecting the display-archive flag."""
    if display_archive:
        return notes
    return [note for note in notes if not note.archived]


def display_notes(notes: list[Note], style_config: StyleConfig) -> str:
    """Format notes as lines, muting archived ones."""
    if len(notes) != 0:
        lines: list[str] = []
        for note in notes:
            if not note.archived:
                lines.append(f"#{note.id} {note.title}")
            else:
                lines.append(make_muted(f"#{note.id} {note.title}", style_config))
        return "\n".join(lines)
    return make_muted(
        f"No notes yet — press {Constants.KEY_CREATE} to create", style_config
    )


def _get_visible_notes(app: NotesApp, style_config: StyleConfig) -> str:
    """Format queued notifications as red lines."""
    lines: list[str] = [
        make_red("[!] " + notification, style_config)
        for notification in app.pop_notifications()
    ]
    return "\n".join(lines)


def _show_main_menu(app: NotesApp, style_config: StyleConfig) -> str:
    """Compose the full main menu view: header, notes and hints."""
    visible_notes: list[Note] = get_visible_notes(
        app.notes,
        display_archive=app.settings.get_bool_value(Constants.SETTING_SHOW_ARCHIVED),
    )
    header: str = get_header(
        f"CliNotes: {get_date(get_local_now(), app.settings.date_pattern())} "
        f"· {get_plural(len(visible_notes), 'note')}",
        style_config,
    )
    body: str = "\n\n".join(
        section
        for section in [
            _get_visible_notes(app, style_config),
            display_notes(visible_notes, style_config),
        ]
        if section
    )

    hints: str = make_hint(
        "Actions: {ID}"
        f" - open note; {Constants.KEY_QUIT} - quit; {Constants.KEY_CREATE} - create; "
        f"{Constants.KEY_SEARCH} - search; "
        f"{Constants.KEY_TOGGLE_ARCHIVED} - show archived; "
        f"{Constants.KEY_SETTINGS} - settings",
        style_config,
    )

    return build_view(header, body, hints)


def display_main_menu(app: NotesApp, style_config: StyleConfig) -> str:
    """Clear the screen, print the main menu and read an action."""
    clear_screen(style_config)
    print(_show_main_menu(app, style_config))  # noqa: T201
    return read_input()
