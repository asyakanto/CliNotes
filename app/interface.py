from os import name, system


def clear_screen():
    if name == "nt":
        system("cls")
    else:
        system("clear")


def display_notes(notes):
    result = ""
    for note in notes:
        result += f"#{note.id} {note.title}" + "\n"
        result += (note.text if note.text else "-") + "\n"
        tags_str = ", ".join(note.tags)
        result += "@: " + mk_muted(tags_str) + "\n" if note.tags else ""
        result += f"{'=' * 40}" + "\n\n"
    return result


def display_notes_names(notes):
    result = ""
    for note in notes:
        result += f"#{note.id} {note.title}" + "\n"
    return result


def mk_error(text):
    return "\033[31m" + text + "\033[0m"


def mk_success(text):
    return "\033[32m" + text + "\033[0m"


def mk_warning(text):
    return "\033[33m" + text + "\033[0m"


def mk_prompt(text):
    return "\033[36m" + text + "\033[0m"


def mk_muted(text):
    return "\033[2m" + text + "\033[0m"
