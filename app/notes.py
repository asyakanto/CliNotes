from dataclasses import dataclass
from datetime import datetime
from app.constants import TAG_PREFIXES, DEFAULT_ARCHIVED_AT
import re


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


def get_tags(text: str) -> list[str]:
    tags: list[str] = []
    rest: str
    parts: list[str]
    pattern: str = "|".join(map(re.escape, TAG_PREFIXES))
    for word in text.split():
        for prefix in TAG_PREFIXES:
            if word.startswith(prefix):
                rest = word[len(prefix) :]
                parts = re.split(pattern, rest)
                for part in parts:
                    if part and part not in tags:
                        tags.append(part)
                break
    return tags
