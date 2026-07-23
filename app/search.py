from app.models import Note
from app.constants import TAG_PREFIXES, KEY_SEARCH_QUIT


def merge_prefixes(tokens: list[str]) -> list[str]:
    current_token: str = ""
    merged_tokens: list[str] = []
    for token in tokens:
        if token.startswith("title:") or token.startswith("text:"):
            if current_token:
                merged_tokens.append(current_token)
            current_token = token
        else:
            merged_tokens.append(current_token + token)
            current_token = ""
    if current_token:
        merged_tokens.append(current_token)
    return merged_tokens


def split_with_quotes(query: str) -> list[str]:
    tokens: list[str] = []
    current_token: str = ""
    in_quotes: bool = False
    for char in query:
        if char == '"':
            in_quotes = not in_quotes
        elif char == " " and not in_quotes:
            if current_token:
                tokens.append(current_token.strip().lower())
                current_token = ""
        else:
            current_token += char
    if current_token:
        tokens.append(current_token.strip().lower())
    return tokens


def parse_query(query: str) -> list[tuple[str, str]]:
    raw_parts: list[str] = split_with_quotes(query)
    raw_parts = merge_prefixes(raw_parts)
    filters: list[tuple[str, str]] = []

    for part in raw_parts:
        is_tag: bool = False
        for prefix in TAG_PREFIXES:
            if part.strip().startswith(prefix):
                filters.append(("tag", part.removeprefix(prefix).strip()))
                is_tag = True
                break
        if is_tag:
            continue

        if part.strip().startswith("title:"):
            filters.append(("title", part.removeprefix("title:").strip()))
        elif part.strip().startswith("text:"):
            filters.append(("text", part.removeprefix("text:").strip()))
        else:
            filters.append(("all", part.strip()))

    return filters


def apply_filters(notes: list[Note], filters: list[tuple[str, str]]) -> list[Note]:
    results: list[Note] = notes
    for filter_type, filter_value in filters:
        if filter_value:
            filtered: list[Note] = []
            filter_value_lower = filter_value.lower()
            for note in results:
                match filter_type:
                    case "all":
                        if (
                            filter_value_lower in note.title.lower()
                            or filter_value_lower in note.text.lower()
                        ):
                            if note not in filtered:
                                filtered.append(note)
                        for tag in note.tags:
                            if filter_value_lower in tag.lower():
                                if note not in filtered:
                                    filtered.append(note)
                                break
                    case "tag":
                        for tag in note.tags:
                            if filter_value_lower in tag.lower():
                                if note not in filtered:
                                    filtered.append(note)
                                break
                    case "title":
                        if filter_value_lower in note.title.lower():
                            if note not in filtered:
                                filtered.append(note)
                    case "text":
                        if filter_value_lower in note.text.lower():
                            if note not in filtered:
                                filtered.append(note)
                    case _:
                        continue
            results = filtered
    return results


def search_help() -> str:
    return f"""╭─ Search help ──────────────────────────────╮
│ word           — search in title & text    │
│ @tag  #tag     — search by tag             │
│ title:word     — search in title only      │
│ text:word      — search in text only       │
│ "word"         — search exact phrase       │
│ title:"phrase" — exact phrase in title     │
│ text:"phrase"  — exact phrase in text      │
│                                            │
│ Combine filters with spaces: AND logic     │
│ Example: @work title:"meeting notes"       │
│                                            │
│ {KEY_SEARCH_QUIT}             — quit search               │
╰────────────────────────────────────────────╯"""
