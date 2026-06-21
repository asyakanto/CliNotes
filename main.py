from datetime import datetime
from prompt_toolkit import prompt

from app.interface import (
    clear_screen,
    display_notes,
    display_notes_names,
    mk_error,
    mk_success,
    mk_warning,
    mk_prompt,
    mk_muted,
)
from app.notes import get_tags, get_date
from app.app import NotesApp

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
    ],
)


def main() -> None:

    app = NotesApp()
    logging.info("Application started")

    while True:
        clear_screen()

        print(
            """
1. Create Note
2. Show Notes
3. Edit Note
4. Delete Note
5. Search Notes
6. Exit
"""
        )

        mode = input(mk_prompt("Choose an action: "))
        print()

        if mode == "1":
            title = input(mk_prompt("Note Name: "))
            text = input(mk_prompt("Text: "))
            tags = get_tags(text)
            date = get_date(datetime.now())
            tags.insert(0, date)

            result = app.create_note(title, text, tags)

            print()
            if result is None:
                print(mk_error("Title cannot be empty"))
            else:
                print(mk_success(f"Note #{result.id} {result.title} created"))

        elif mode == "2":
            if app.notes:
                result = display_notes(app.notes)
                print(result, end="")
            else:
                print(mk_warning("No notes yet"))

        elif mode == "3":
            if app.notes:
                result = display_notes_names(app.notes)
                print(result)
                try:
                    id_of_editing_note = int(
                        input(
                            mk_prompt(
                                "Print ID of the note you want to edit (-1 to exit): "
                            )
                        )
                    )
                    print()
                    if id_of_editing_note >= 0:
                        note = app.get_note(id_of_editing_note)
                        if note is not None:
                            title = note.title
                            text = note.text
                            tags = note.tags
                            while True:
                                clear_screen()

                                editing_mode = input(
                                    mk_prompt(
                                        f"""
1. Title: \"{title}\"
2. Text: \"{text}\"
3. Tags: {tags}
4. Save and exit

Choose editing mode: """
                                    )
                                )
                                if editing_mode == "1":
                                    new_title = prompt("New title: ", default=title)
                                    if new_title.strip():
                                        title = new_title
                                elif editing_mode == "2":
                                    new_text = prompt("New text: ", default=text)
                                    if new_text.strip():
                                        text = new_text
                                elif editing_mode == "3":
                                    pass
                                elif editing_mode == "4":
                                    app.edit_note(id_of_editing_note, title, text, tags)
                                    break
                                else:
                                    print(mk_error("Wrong action"))

                                input(mk_muted("\nPress Enter to continue..."))
                        else:
                            print(mk_error("There's no note with such ID"))
                    else:
                        continue

                except ValueError:
                    print(mk_error("That's not a number"))
            else:
                print(mk_warning("No notes yet"))

        elif mode == "4":
            if app.notes:
                result = display_notes_names(app.notes)
                print(result)
                try:
                    id_of_deleting_note = int(
                        input(
                            mk_prompt(
                                "Print ID of the note you want to delete (-1 to exit): "
                            )
                        )
                    )
                    print()
                    if id_of_deleting_note >= 0:
                        is_deleted = app.delete_note(id_of_deleting_note)
                        if is_deleted:
                            print(
                                mk_success(
                                    f"Note with ID {id_of_deleting_note} deleted"
                                )
                            )
                        else:
                            print(mk_error("There's no note with such ID"))
                    else:
                        continue
                except ValueError:
                    print(mk_error("That's not a number"))

        elif mode == "5":
            search = input(
                mk_prompt("Search by name (start with @ to enable tag search): ")
            )
            print()
            found_notes = app.search_notes(search)
            if found_notes:
                result = display_notes(found_notes)
                print(result, end="")
            else:
                print(mk_warning("Nothing found"))

        elif mode == "6":
            logging.info("Application closed")
            clear_screen()
            break

        else:
            print(mk_error("Wrong action"))

        input(mk_muted("\nPress Enter to continue..."))


if __name__ == "__main__":
    main()