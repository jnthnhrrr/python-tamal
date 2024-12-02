from types import new_class
from typing import TypeAlias

from .defaults import DEFAULT_HYPHEN, DEFAULT_HYPHENS, DEFAULT_SOFT_HYPHEN

Head: TypeAlias = str
Tail: TypeAlias = str


def _visible_index(text: str, length: int, soft_hyphen: str) -> int:
    """The index where the count of visible characters equals `length`"""
    invisible = 0
    index = length
    while True:
        extended_invisible = text[:index].count(soft_hyphen)
        new_invisible = extended_invisible - invisible
        if not new_invisible:
            break
        index += new_invisible
        invisible = extended_invisible
    return index


def break_text(
    text: str,
    width: int,
    hyphen: str = DEFAULT_HYPHEN,
    soft_hyphen: str = DEFAULT_SOFT_HYPHEN,
    hyphens: set[str] = DEFAULT_HYPHENS,
) -> tuple[Head, Tail]:
    width = _visible_index(text, width, soft_hyphen)
    if len(text) <= width:
        return text, ""
    for reverse_index, char in enumerate(reversed(text[:width])):
        index = width - reverse_index
        if char == " ":
            return text[: index - 1], text[index:]
        if char in hyphens:
            return text[:index], text[index:]
        if char == soft_hyphen:
            return text[: index - 1] + hyphen, text[index:]

    return (text[: width - 1] + hyphen, text[width - 1 :])
