import re
from dataclasses import dataclass
from datetime import datetime

from app.constants import Constants as C


@dataclass
class Note:
    title: str
    text: str
    tags: list[str]
    created: str
    id: int | None = None
    archived: bool = False
    archived_at: str = C.DEFAULT_ARCHIVED_AT


def get_date(dt: datetime, date_format: str) -> str:
    return dt.strftime(date_format)


def get_tags(text: str, prefixes: list[str]) -> list[str]:
    tags: list[str] = []
    _PATTERN: str = "|".join(map(re.escape, prefixes))
    for word in text.split():
        for prefix in prefixes:
            if word.startswith(prefix):
                rest: str = word[len(prefix) :]
                parts: list[str] = re.split(_PATTERN, rest)
                for part in parts:
                    if part and part not in tags:
                        tags.append(part)
                break
    if has_easter_egg(text) and C.EASTER_EGG not in tags:
        tags.append("<3")
    return tags


def get_local_now() -> datetime:
    return datetime.now().astimezone()


def get_date_format(display_key: str) -> str:
    try:
        date_format = C.DATE_FORMAT_MAP[display_key]
    except KeyError:
        date_format = "%d-%m-%Y"
    return date_format


def has_easter_egg(text: str) -> bool:

    return all(condition in text.lower() for condition in C.EASTER_EGG_CONDITIONS)
