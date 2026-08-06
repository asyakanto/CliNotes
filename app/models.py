import re
from dataclasses import dataclass
from datetime import datetime

from app.constants import DEFAULT_ARCHIVED_AT, TAG_PREFIXES


@dataclass
class Note:
    title: str
    text: str
    tags: list[str]
    created: str
    id: int | None = None
    archived: bool = False
    archived_at: str = DEFAULT_ARCHIVED_AT


def get_date(dt: datetime) -> str:
    return f"{dt.day:02d}-{dt.month:02d}-{dt.year}"


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
