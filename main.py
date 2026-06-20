from datetime import datetime

from app.interface import (
    clear_screen,
    mk_prompt,
    print_error,
    print_warning,
)
from app.notes import (
    add_id,
    create_note,
    delete_note,
    display_notes,
    display_notes_names,
    get_date,
    get_max_id,
    get_tags,
    search_notes,
)
from app.storage import load_notes


def main():
    notes = load_notes()
    max_id, notes_with_no_id = get_max_id(notes)
    if notes_with_no_id:
        max_id = add_id(notes, max_id)

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
            title = input("Note Name: ")
            text = input("Text: ")
            tags = get_tags(text)
            date = get_date(datetime.now())
            tags.insert(0, date)
            max_id += 1
            result = create_note(notes, title, text, tags, max_id)
            print()
            print(result)

        elif mode == "2":
            if notes:
                result = display_notes(notes)
                print(result, end="")
            else:
                print_warning("No notes yet")

        elif mode == "3":
            if notes:
                result = display_notes_names(notes)
                print(result)
                try:
                    number_of_deleting_note = int(
                        input(
                            "Print number of the note you want to delete (0 to exit): "
                        )
                    )
                    print()
                    if number_of_deleting_note > 0:
                        res = delete_note(notes, number_of_deleting_note)
                        print(res)
                    elif number_of_deleting_note < 0:
                        print_error("There's no note with such number")
                    else:
                        continue
                except ValueError:
                    print_error("That's not a number")
            else:
                print_warning("No notes yet")

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
                print_warning("Nothing found")

        elif mode == "5":
            break

        else:
            print_error("Wrong action")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
