import re
from dataclasses import dataclass
from datetime import datetime

from app.constants import DATE_FORMAT_MAP, DEFAULT_ARCHIVED_AT, TAG_PREFIXES


@dataclass
class Note:
    title: str
    text: str
    tags: list[str]
    created: str
    id: int | None = None
    archived: bool = False
    archived_at: str = DEFAULT_ARCHIVED_AT


def get_date(dt: datetime, date_format: str) -> str:
    return dt.strftime(date_format)


_PATTERN: str = "|".join(map(re.escape, TAG_PREFIXES))


def get_tags(text: str) -> list[str]:
    tags: list[str] = []
    for word in text.split():
        for prefix in TAG_PREFIXES:
            if word.startswith(prefix):
                rest: str = word[len(prefix) :]
                parts: list[str] = re.split(_PATTERN, rest)
                for part in parts:
                    if part and part not in tags:
                        tags.append(part)
                break
    return tags


def get_local_now() -> datetime:
    return datetime.now().astimezone()


def get_date_format(display_key: str) -> str:
    try:
        date_format = DATE_FORMAT_MAP[display_key]
    except KeyError:
        date_format = "%d-%m-%Y"
    return date_format
