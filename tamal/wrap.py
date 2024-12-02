from re import search
from typing import TypeAlias

from .defaults import (
    DEFAULT_HYPHEN,
    DEFAULT_HYPHENS,
    DEFAULT_PARAGRAPH,
    DEFAULT_SOFT_HYPHEN,
    DEFAULT_WHITESPACE,
)

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


def _latest_occurrence(pattern: str, text: str) -> int:
    """index of start of latest occurrence of pattern in text"""
    match = search(f"(?s:.*){pattern}", text)
    if match:
        return match.end() - len(pattern)
    return 0


def break_text(
    text: str,
    width: int,
    hyphen: str = DEFAULT_HYPHEN,
    soft_hyphen: str = DEFAULT_SOFT_HYPHEN,
    hyphens: set[str] = DEFAULT_HYPHENS,
    whitespace: set[str] = DEFAULT_WHITESPACE,
) -> tuple[Head, Tail]:
    hyphens.add(hyphen)
    width = _visible_index(text, width, soft_hyphen)
    if len(text) <= width:
        return text, ""
    # Sorting break_strings so that longer hyphens prevail in break_indices
    break_strings = sorted(
        list(hyphens | {soft_hyphen} | whitespace), key=lambda s: len(s)
    )
    break_indices = {
        _latest_occurrence(char, text[: width + len(char) - 1]): char
        for char in break_strings
    }
    break_index = max(break_indices.keys())
    if not break_index:
        return (text[: width - 1] + hyphen, text[width - 1 :])

    char = break_indices[break_index]
    if char in whitespace:
        return text[:break_index], text[break_index + len(char) :]
    if char in hyphens:
        break_index += len(char)
        return (text[:break_index], text[break_index:])
    if char == soft_hyphen:
        # Replacing the soft hyphen with a hyphen when breaking at it
        return (
            text[:break_index] + hyphen,
            text[break_index + len(char) :],
        )
    raise Exception("Shouldn't be getting here")


def break_all(
    text: str,
    width: int,
    hyphen: str = DEFAULT_HYPHEN,
    soft_hyphen: str = DEFAULT_SOFT_HYPHEN,
    hyphens: set[str] = DEFAULT_HYPHENS,
    whitespace: set[str] = DEFAULT_WHITESPACE,
) -> list[str]:
    lines = []
    while True:
        head, tail = break_text(
            text=text,
            width=width,
            hyphen=hyphen,
            soft_hyphen=soft_hyphen,
            hyphens=hyphens,
            whitespace=whitespace,
        )
        for blank in whitespace:
            head = head.replace(blank, " ")
        lines.append(head)
        if not tail:
            break
        text = tail
    return lines


def wrap(
    text: str,
    width: int,
    hyphen: str = DEFAULT_HYPHEN,
    soft_hyphen: str = DEFAULT_SOFT_HYPHEN,
    hyphens: set[str] = DEFAULT_HYPHENS,
    whitespace: set[str] = DEFAULT_WHITESPACE,
    paragraph: str = DEFAULT_PARAGRAPH,
) -> str:
    chunks = text.split(paragraph)
    wrapped_chunks = []
    for chunk in chunks:
        wrapped_chunks.append(
            "\n".join(
                break_all(
                    chunk,
                    width=width,
                    hyphen=hyphen,
                    soft_hyphen=soft_hyphen,
                    hyphens=hyphens,
                    whitespace=whitespace,
                )
            )
        )
    return "\n\n".join(wrapped_chunks)
