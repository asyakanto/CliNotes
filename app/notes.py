from app.storage import save_notes
from app.interface import mk_error, mk_success, mk_tags

def create_note(notes, title, text, tags, idd):
    if not title.strip():
        return mk_error("Title cannot be empty")
    note = {"title": title, "text": text, "tags": tags, "id": idd}
    notes.append(note)
    save_notes(notes)
    return mk_success(f"Note {title} created")

def display_notes(notes):
    result = ""
    for i, note in enumerate(notes, 1):
        result += f"#{i} {note['title']}" + "\n"
        result += (note['text'] if note['text'] else "-") + "\n"
        tags_str = ", ".join(note.get("tags", []))
        result += ("@: " + mk_tags(tags_str) + "\n" if note.get("tags", []) else "")
        result += f"{'='*40}" + "\n\n"
    return result

def display_notes_names(notes):
    result = ""
    for i, note in enumerate(notes, 1):
        result += f"#{i} {note['title']}" + "\n"
    return result

def delete_note(notes, number):
    if len(notes) < number:
        return mk_error("There's no note with such number")
    notes.pop(number - 1)
    save_notes(notes)
    return mk_success(f"Note number {number} deleted")

def search_notes(notes, search):
    if not search:
        return notes

    search = search.lower()
    found_notes = []
    search_by = "title"

    if search[0] == "@":
        search=search[1:]
        search_by = "tags"

    
    if search_by == "title":
        for i in notes:
            if search in i[search_by].lower():
                found_notes.append(i)
    elif search_by == "tags":
        for i in notes:
            for j in i.get("tags", []):
                if search in j:
                    found_notes.append(i)
                    break

    return found_notes

def get_max_id(notes):
    max_id = -1
    notes_with_no_id = False
    for note in notes:
        note_id = note.get("id")
        if note_id != None:
            if note_id > max_id:
                max_id = note_id
        else:
            notes_with_no_id = True
    return max_id, notes_with_no_id

def add_id(notes, max_id):
    for note in notes:
        if note.get("id") == None:
            max_id += 1
            note["id"] = max_id
    save_notes(notes)
    return max_id

def get_date(dt):
    return f"{dt.day:02d}-{dt.month:02d}-{dt.year}"

def get_tags(text):
    sims = ["@", "#"]
    tags = []
    for s in sims:
        if s in text:
            current_text=text
            while s in current_text:
                index_of_s = current_text.index(s)
                if index_of_s != 0 and current_text[index_of_s - 1] == "\\":
                    current_text = current_text[index_of_s + 2 : ]
                else:
                    current_text = current_text[index_of_s + 1 : ]
                    min_word = None
                    for i in (sims+[" ", "\n", "\t"]):
                        word = current_text.split(i).pop(0)
                        if min_word:
                            if len(word) < len(min_word):
                                min_word = word
                        else:
                            min_word = word
                    if min_word and min_word not in tags:
                        tags.append(min_word)
                    current_text = current_text[len(min_word):]

        else:
            continue
    return tags