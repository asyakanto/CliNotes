from datetime import datetime

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
from app.notes import (
    get_max_id,
    get_tags,
    get_date,
    create_note,
    delete_note,
    search_notes,
)
from app.storage import load_notes


def main():

    notes = load_notes()
    max_id = get_max_id(notes)

    while True:
        clear_screen()

        print(
            """
1. Create Note
2. Show Notes
3. Delete Note
4. Search Notes
5. Exit
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
            max_id = get_max_id(notes) + 1

            result = create_note(notes, title, text, tags, max_id)

            print()
            if result is None:
                print(mk_error("Title cannot be empty"))
            else:
                print(mk_success(f"Note #{result.id} {result.title} created"))

        elif mode == "2":
            if notes:
                result = display_notes(notes)
                print(result, end="")
            else:
                print(mk_warning("No notes yet"))

        elif mode == "3":
            if notes:
                result = display_notes_names(notes)
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
                        is_deleted = delete_note(notes, id_of_deleting_note)
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
            else:
                print(mk_warning("No notes yet"))

        elif mode == "4":
            search = input(
                mk_prompt("Search by name (start with @ to enable tag search): ")
            )
            print()
            found_notes = search_notes(notes, search)
            if found_notes:
                result = display_notes(found_notes)
                print(result, end="")
            else:
                print(mk_warning("Nothing found"))

        elif mode == "5":
            break

        else:
            print(mk_error("Wrong action"))

        input(mk_muted("\nPress Enter to continue..."))


if __name__ == "__main__":
    main()
