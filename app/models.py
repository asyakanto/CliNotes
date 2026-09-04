"""Data models for notes, plus helpers for date/tag/plural handling."""

import re
from dataclasses import dataclass
from datetime import datetime
from typing import TypedDict

from app.constants import Constants


@dataclass
class Note:
    """A single note with title, text, tags and archiving metadata."""

    title: str
    text: str
    tags: list[str]
    created: str
    id: int | None = None
    archived: bool = False
    archived_at: str = Constants.DEFAULT_ARCHIVED_AT


class NoteDict(TypedDict):
    """The JSON shape of a note as stored in the data file."""

    title: str
    text: str
    tags: list[str]
    created: str
    id: int | None
    archived: bool
    archived_at: str


def get_date(dt: datetime, date_format: str) -> str:
    """Format a datetime according to the given format string."""
    return dt.strftime(date_format)


def get_tags(text: str, prefixes: list[str]) -> list[str]:
    """Extract tagged words from a text.

    Args:
        text (str): The full note text to scan.
        prefixes (list[str]): Tag prefixes (e.g. "#") to look for.

    Returns:
        list[str]: Unique tags found, plus an easter-egg tag if applicable.

    """
    tags: list[str] = []
    pattern: str = "|".join(map(re.escape, prefixes))
    for word in text.split():
        for prefix in prefixes:
            if word.startswith(prefix):
                rest: str = word[len(prefix) :]
                parts: list[str] = re.split(pattern, rest)
                for part in parts:
                    if part and part not in tags:
                        tags.append(part)
                break
    if has_easter_egg(text) and Constants.EASTER_EGG not in tags:
        tags.append("<3")
    return tags


def get_local_now() -> datetime:
    """Return current time in user's timezone."""
    return datetime.now().astimezone()


def get_date_format(display_key: str) -> str:
    """Return date format from constants by key in settings."""
    try:
        date_format = Constants.DATE_FORMAT_MAP[display_key]
    except KeyError:
        date_format = "%d-%m-%Y"
    return date_format


def has_easter_egg(text: str) -> bool:
    """Check whether the text contains all words needed for an easter egg."""
    return all(
        condition in text.lower() for condition in Constants.EASTER_EGG_CONDITIONS
    )


def get_plural(num: int, string: str) -> str:
    """Return the word form matching the given count."""
    if num == 1:
        return f"{num} {string}"
    return f"{num} {string}s"
