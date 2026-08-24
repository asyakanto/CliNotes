from app.app import NotesApp
from app.constants import Constants as C
from app.models import Note
from app.ui_input import pause, prompt_input
from app.ui_menu import display_notes, get_visible_notes
from app.ui_note import open_note
from app.ui_style import clear_screen, get_header, make_box


def create_note_scenario(app: NotesApp) -> None:
    title: str = prompt_input(lowercase=False, hint="Note Name")
    while not title:
        title = prompt_input(
            hint="Title cannot be empty. Note Name", lowercase=False, danger=True
        )
    if title == C.KEY_PERCENT_QUIT:
        return
    text: str = prompt_input(hint="Text", lowercase=False)
    note: Note = app.create_note(title, text)
    open_note(app, note)


def search_scenario(app: NotesApp) -> None:
    query: str = prompt_input(
        hint=f"Enter a search query ({C.KEY_SEARCH_HELP} for help)"
    )
    while query == C.KEY_SEARCH_HELP:
        print(search_help(app.settings.active_tag_prefixes()))
        query = prompt_input(
            hint=f"Enter a search query ({C.KEY_SEARCH_HELP} for help)"
        )
    if query == C.KEY_PERCENT_QUIT:
        return
    results: list[Note] = app.search_note(query)
    if not results:
        pause("Nothing found")
    else:
        while True:
            clear_screen()
            print(
                get_header(
                    f"Search results: {len(results)} {'notes' if len(results) != 1 and len(results) != 0 else 'note'}"
                )
            )
            print(display_notes(get_visible_notes(results, True)))

            note_mode: str = prompt_input(
                hint=f"Enter ID to open, {C.KEY_QUIT} to go back"
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
    Wid: int = max(len(l) for l, r in pairs)
    lines: list[str] = []
    for l, r in pairs:
        if not l and not r:
            lines.append("")
        else:
            lines.append(f"{l:<{Wid}}— {r}")
    lines.append("Combine filters with spaces: AND logic")
    lines.append(
        f'{prefixes[0] + "work " if len(prefixes) else ""}text:"123 123" title:"meeting notes"'
    )
    return make_box(lines, "Search help")
