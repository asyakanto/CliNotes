from app.models import Note


def merge_prefixes(tokens: list[str]) -> list[str]:
    current_token: str = ""
    merged_tokens: list[str] = []
    for token in tokens:
        if token.startswith(("title:", "text:")):
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
        match char:
            case '"':
                in_quotes = not in_quotes
            case " ":
                if not in_quotes and current_token:
                    tokens.append(current_token.strip().lower())
                    current_token = ""
            case _:
                current_token += char
    if current_token:
        tokens.append(current_token.strip().lower())
    return tokens


def parse_query(query: str, prefixes: list[str]) -> list[tuple[str, str]]:
    raw_parts: list[str] = split_with_quotes(query)
    raw_parts = merge_prefixes(raw_parts)
    filters: list[tuple[str, str]] = []

    for part in raw_parts:
        is_tag: bool = False
        for prefix in prefixes:
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
                        ) and note not in filtered:
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
                        if (
                            filter_value_lower in note.title.lower()
                            and note not in filtered
                        ):
                            filtered.append(note)
                    case "text":
                        if (
                            filter_value_lower in note.text.lower()
                            and note not in filtered
                        ):
                            filtered.append(note)
                    case _:
                        continue
            results = filtered
    return results
