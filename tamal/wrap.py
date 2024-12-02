from re import search
from types import new_class
from typing import TypeAlias

from .defaults import DEFAULT_HYPHEN, DEFAULT_HYPHENS, DEFAULT_SOFT_HYPHEN

Head: TypeAlias = str
Tail: TypeAlias = str


def _visible_index(text: str, length: int, soft_hyphen: str) -> int:
    """The index where the count of visible characters equals `length`"""
    invisible = 0
    # in case soft_hyphen is a multichar string, the soft hyphen might be split
    # at index `length`
    index = length + len(soft_hyphen) - 1
    while True:
        extended_invisible = text[:index].count(soft_hyphen) * len(soft_hyphen)
        new_invisible = extended_invisible - invisible
        if not new_invisible:
            break
        index += new_invisible
        invisible = extended_invisible
    return index


def _latest_occurence(pattern: str, text: str) -> int:
    match = search(f"(?s:.*){pattern}", text)
    if match:
        return match.end()
    return 0


def break_text(
    text: str,
    width: int,
    hyphen: str = DEFAULT_HYPHEN,
    soft_hyphen: str = DEFAULT_SOFT_HYPHEN,
    hyphens: set[str] = DEFAULT_HYPHENS,
) -> tuple[Head, Tail]:
    hyphens.add(hyphen)
    width = _visible_index(text, width, soft_hyphen)
    if len(text) <= width:
        return text, ""
    break_indices = {
        _latest_occurence(char, text[:width]): char
        for char in hyphens | {soft_hyphen, " "}
    }
    break_index = max(break_indices.keys())
    if not break_index:
        return (text[: width - 1] + hyphen, text[width - 1 :])

    char = break_indices[break_index]
    if char == " ":
        return text[: break_index - 1], text[break_index:]
    if char in hyphens:
        return text[:break_index], text[break_index:]
    if char == soft_hyphen:
        break_index = break_index - len(soft_hyphen)
        return (
            text[:break_index] + hyphen,
            text[break_index + len(soft_hyphen) :],
        )
