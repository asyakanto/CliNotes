from dataclasses import dataclass
from datetime import datetime
from app.constants import TAG_PREFIXES, TAG_SEPARATORS


@dataclass
class Note:
    title: str
    text: str
    tags: list[str]
    created: str
    id: int = None
    archived: bool = False
    archived_at: str = "0"


def get_date(dt: datetime) -> str:
    return f"{dt.day:02d}-{dt.month:02d}-{dt.year}"


def get_tags(text: str) -> list[str]:
    tags = []
    for s in TAG_PREFIXES:
        if s in text:
            current_text = text
            while s in current_text:
                index_of_s = current_text.index(s)
                if index_of_s != 0 and current_text[index_of_s - 1] == "\\":
                    current_text = current_text[index_of_s + 2 :]
                else:
                    current_text = current_text[index_of_s + 1 :]
                    min_word = None
                    for i in TAG_PREFIXES + TAG_SEPARATORS:
                        word = current_text.split(i).pop(0)
                        if min_word:
                            if len(word) < len(min_word):
                                min_word = word
                        else:
                            min_word = word
                    if min_word and min_word not in tags:
                        tags.append(min_word)
                    current_text = current_text[len(min_word) :]
        else:
            continue
    return tags
