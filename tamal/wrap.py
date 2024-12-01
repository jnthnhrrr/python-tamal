from typing import TypeAlias
from .defaults import DEFAULT_HYPHEN, DEFAULT_HYPHENS, DEFAULT_SOFT_HYPHENS

Head: TypeAlias = str
Tail: TypeAlias = str

def break_text(
    text: str,
    width: int,
    hyphen: str = DEFAULT_HYPHEN,
    hyphens: set[str] = DEFAULT_HYPHENS,
    soft_hyphens: set[str] = DEFAULT_SOFT_HYPHENS,
) -> tuple[Head, Tail]:
    if len(text) <= width:
        return text, ""

    for (reverse_index, char) in enumerate(reversed(text[:width])):
        index = width - reverse_index
        if char == " ":
            return text[:index-1], text[index:]
        if char in hyphens:
            return text[:index], text[index:]