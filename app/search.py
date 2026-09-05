"""Search and filtering logic for notes."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import Note


def _merge_prefixes(tokens: list[str]) -> list[str]:
    """Merge tokens that follow a 'title:'/'text:' prefix into one token.

    Args:
        tokens (list[str]): The raw list of string tokens.

    Returns:
        list[str]: Tokens with prefixed fragments merged tohether.

    """
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


def _split_with_quotes(query: str) -> list[str]:
    """Split a query into tokens, keeping quoted phrases together.

    Args:
        query (str): the raw search query string.

    Returns:
        list[str]: lowercased tokens. respecting quoted groups.

    """
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
    """Parse a search query into a list of (filter_type, value) pairs.

    Args:
        query (str): The raw search query string.
        prefixes (list[str]): Tag prefixes (e.g. "#") used to detect tags.

    Returns:
        list[tuple[str, str]]: Pairs like ("tag", value), ("title", ...),
            ("text", ...) or ("all", ...).

    """
    raw_parts: list[str] = _split_with_quotes(query)
    raw_parts = _merge_prefixes(raw_parts)
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
    """Filter notes by successively applying each search filter.

    Args:
        notes (list[Note]): The list of notes to filter.
        filters (list[tuple[str, str]]): (filter_type, value) pairs.

    Returns:
        list[Note]: The notes that match all filters.

    """
    results: list[Note] = notes
    for filter_type, filter_value in filters:
        if filter_value:
            low: str = filter_value.lower()
            results = [n for n in results if _note_matches(filter_type, low, n)]

    return results


def _note_matches(filter_type: str, low: str, n: Note) -> bool:
    match filter_type:
        case "all":
            return any(
                [_matches_text(low, n), _matches_title(low, n), _matches_tag(low, n)]
            )
        case "tag":
            return _matches_tag(low, n)
        case "title":
            return _matches_title(low, n)
        case "text":
            return _matches_text(low, n)
        case _:
            return False


def _matches_tag(low: str, n: Note) -> bool:
    return any(low in tag.lower() for tag in n.tags)


def _matches_text(low: str, n: Note) -> bool:
    return low in n.text.lower()


def _matches_title(low: str, n: Note) -> bool:
    return low in n.title.lower()
