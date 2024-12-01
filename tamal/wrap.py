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
