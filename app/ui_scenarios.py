from app.app import NotesApp
from app.constants import Constants as C
from app.models import Note, get_plural
from app.ui_input import pause, prompt_input
from app.ui_menu import display_notes, get_visible_notes
from app.ui_note import open_note
from app.ui_style import StyleConfig, clear_screen, get_header, make_box


def create_note_scenario(app: NotesApp, style_config: StyleConfig) -> None:
    title: str = prompt_input(
        lowercase=False, hint="Note Name", style_config=style_config
    )
    while not title:
        title = prompt_input(
            hint="Title cannot be empty. Note Name",
            lowercase=False,
            danger=True,
            style_config=style_config,
        )
    if title == C.KEY_PERCENT_QUIT:
        return
    text: str = prompt_input(hint="Text", lowercase=False, style_config=style_config)
    note: Note = app.create_note(title, text)
    open_note(app, note, style_config)


def search_scenario(app: NotesApp, style_config: StyleConfig) -> None:
    query: str = prompt_input(
        hint=f"Enter a search query ({C.KEY_SEARCH_HELP} for help)",
        style_config=style_config,
    )
    while query == C.KEY_SEARCH_HELP:
        print(search_help(app.settings.active_tag_prefixes()))
        query = prompt_input(
            hint=f"Enter a search query ({C.KEY_SEARCH_HELP} for help)",
            style_config=style_config,
        )
    if query == C.KEY_PERCENT_QUIT:
        return
    results: list[Note] = app.search_note(query)
    if not results:
        pause("Nothing found", style_config)
    else:
        while True:
            clear_screen(style_config)
            print(
                get_header(
                    f"Search results: {get_plural(len(results), 'note')}", style_config
                )
            )
            print(display_notes(get_visible_notes(results, True), style_config))

            note_mode: str = prompt_input(
                hint=f"Enter ID to open, {C.KEY_QUIT} to go back",
                style_config=style_config,
            )
            if note_mode == C.KEY_QUIT:
                break
            if (
                note_mode.isdigit()
                and isinstance(note_mode, int)
                and not isinstance(note_mode, bool)
            ):
                found_note: Note | None = app.get_note(int(note_mode))
                if found_note in results:
                    open_note(app, found_note)


def search_help(prefixes: list[str]) -> str:
    pairs: list[tuple[str, str]] = [
        ("word", "search in title & text"),
        *((f"{p}tag", "search by tag") for p in prefixes),
        ("title:word", "search in title only"),
        ("text:word", "search in text only"),
        ('"word"', "search exact phrase"),
        ('title:"phrase"', "exact phrase in title"),
        ('text:"phrase"', "exact phrase in text"),
        ("", ""),
        (C.KEY_PERCENT_QUIT, "quit search"),
        ("", ""),
    ]
    Wid: int = max(len(left) for left, right in pairs)
    lines: list[str] = []
    for left, right in pairs:
        if not left and not right:
            lines.append("")
        else:
            lines.append(f"{left:<{Wid}}— {right}")
    lines.append("Combine filters with spaces: AND logic")
    lines.append(
        f"{prefixes[0] + 'work ' if len(prefixes) else ''}"
        'text:"123 123" title:"meeting notes"'
    )
    return make_box(lines, "Search help")
