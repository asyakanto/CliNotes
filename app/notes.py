from dataclasses import dataclass

@dataclass
class Note:
    title: str
    text: str
    tags: list[str]
    id: int = None

def get_tags(text):
    sims = ["@", "#"]
    tags = []
    for s in sims:
        if s in text:
            current_text = text
            while s in current_text:
                index_of_s = current_text.index(s)
                if index_of_s != 0 and current_text[index_of_s - 1] == "\\":
                    current_text = current_text[index_of_s + 2 :]
                else:
                    current_text = current_text[index_of_s + 1 :]
                    min_word = None
                    for i in sims + [" ", "\n", "\t"]:
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


def get_date(dt):
    return f"{dt.day:02d}-{dt.month:02d}-{dt.year}"