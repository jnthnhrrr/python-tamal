from re import search
from typing import TypeAlias

from tamal.defaults import (
    DEFAULT_HYPHEN,
    DEFAULT_HYPHENS,
    DEFAULT_PARAGRAPH,
    DEFAULT_SOFT_HYPHEN,
    DEFAULT_WHITESPACES,
)

Head: TypeAlias = str
Tail: TypeAlias = str


def _visible_index(text: str, length: int, soft_hyphen: str) -> int:
    """Index where the count of visible characters equals `length`"""
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
    """Index of start of latest occurrence of pattern in text"""
    match = search(f"(?s:.*){pattern}", text)
    if match:
        return match.end() - len(pattern)
    return 0


def chunk(
    text: str,
    width: int,
    hyphen: str = DEFAULT_HYPHEN,
    soft_hyphen: str = DEFAULT_SOFT_HYPHEN,
    hyphens: set[str] = DEFAULT_HYPHENS,
    whitespaces: set[str] = DEFAULT_WHITESPACES,
) -> tuple[Head, Tail]:
    """
    Splitting at hyphens, soft hyphen or whitespace, or forcing a break by
    adding a hyphen,returning the head with maximum width, and the remaining
    tail.

    Parameters:
        text: The text to break.

        width: The target width.

        hyphen: The string to use as hyphen when breaking a word. Can be
            multi-character string.

        soft_hyphen: Soft hyphens existing in the text are used for breaking.
            If a soft hyphen is used for breaking, it will be replaced by a
            hyphen. Soft hyphens are considered "invisible", so they are not
            accounted against the target width. (The idea is that you add soft
            hyphens before breaking, break the text and remove the soft hyphens
            afterwards.) Can be multi-character string.

        hyphens: Existing hyphens in the text are used for breaking (and left
            unchanged). Can be multi-character strings.

        whitespaces: Whitespace strings are used for breaking. Trailing
            whitespace strings at the end of a broken line will be removed. Can
            be multi-character strings.
            paragraph marker.

    Returns:
        Head and Tail.

    Examples:
    ```
    >>> text = 'Hello, World! Nice to meet you.'
    >>> target_width = 15
    >>> chunk(text, target_width)
    ('Hello, World!', 'Nice to meet you.')

    ```
    """
    hyphens.add(hyphen)
    width = _visible_index(text, width, soft_hyphen)
    if len(text) <= width:
        return text, ""
    # Sorting break_strings so that longer hyphens prevail in break_indices
    break_strings = sorted(
        list(hyphens | {soft_hyphen} | whitespaces), key=lambda s: len(s)
    )
    break_indices = {
        _latest_occurrence(char, text[: width + len(char) - 1]): char
        for char in break_strings
    }
    break_index = max(break_indices.keys())
    if not break_index:
        return (text[: width - 1] + hyphen, text[width - 1 :])

    char = break_indices[break_index]
    if char in whitespaces:
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


def break_lines(
    text: str,
    width: int,
    hyphen: str = DEFAULT_HYPHEN,
    soft_hyphen: str = DEFAULT_SOFT_HYPHEN,
    hyphens: set[str] = DEFAULT_HYPHENS,
    whitespaces: set[str] = DEFAULT_WHITESPACES,
) -> list[str]:
    """
    Parameters:
        text: The text to break into lines.

        width: The target width.

        hyphen: The string to use as hyphen when breaking a word. Can be
            multi-character string.

        soft_hyphen: Soft hyphens existing in the text are used for breaking.
            If a soft hyphen is used for breaking, it will be replaced by a
            hyphen. Soft hyphens are considered "invisible", so they are not
            accounted against the target width. (The idea is that you add soft
            hyphens before breaking, break the text and remove the soft hyphens
            afterwards.) Can be multi-character string.

        hyphens: Existing hyphens in the text are used for breaking (and left
            unchanged). Can be multi-character strings.

        whitespaces: Whitespace strings are used for breaking. Trailing
            whitespace strings at the end of a broken line will be removed. Can
            be multi-character strings.
            paragraph marker.

    Returns:
        The resulting lines.

    Examples:
    ```
    >>> text = 'Hello, World! Nice to meet you.'
    >>> target_width = 15
    >>> break_lines(text, target_width)
    ['Hello, World!', 'Nice to meet', 'you.']

    ```
    """
    lines = []
    while True:
        head, tail = chunk(
            text=text,
            width=width,
            hyphen=hyphen,
            soft_hyphen=soft_hyphen,
            hyphens=hyphens,
            whitespaces=whitespaces,
        )
        for blank in whitespaces:
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
    whitespaces: set[str] = DEFAULT_WHITESPACES,
    paragraph: str = DEFAULT_PARAGRAPH,
) -> str:
    """
    Parameters:
        text: The text to wrap.

        width: The target width.

        hyphen: The string to use as hyphen when breaking a word. Can be
            multi-character string.

        soft_hyphen: Soft hyphens existing in the text are used for breaking.
            If a soft hyphen is used for breaking, it will be replaced by a
            hyphen. Soft hyphens are considered "invisible", so they are not
            accounted against the target width. (The idea is that you add soft
            hyphens before wrapping, wrap the text and remove the soft hyphens
            afterwards.) Can be multi-character string.

        hyphens: Existing hyphens in the text are used for breaking (and left
            unchanged). Can be multi-character strings.

        whitespaces: Whitespace strings are used for breaking. Trailing
            whitespace strings at the end of a broken line will be removed. Can
            be multi-character strings.

        paragraph: Marker for the beginning of a new paragraph. Paragraphs will
            remain in the text when wrapping. If you want to treat existing
            line breaks as "hard" line breaks, use the line break chacter as
            paragraph marker.

    Returns:
        The wrapped text as a string.

    Examples:
    ```
    >>> text = "Hello, World!++++Nice to meet you. This text is a bit long."
    >>> target_width = 15
    >>> print(wrap(text, target_width, paragraph="++++"))
    Hello, World!
    <BLANKLINE>
    Nice to meet
    you. This text
    is a bit long.

    ```
    """
    chunks = text.split(paragraph)
    wrapped_chunks = []
    for chunk in chunks:
        wrapped_chunks.append(
            "\n".join(
                break_lines(
                    chunk,
                    width=width,
                    hyphen=hyphen,
                    soft_hyphen=soft_hyphen,
                    hyphens=hyphens,
                    whitespaces=whitespaces,
                )
            )
        )
    return "\n\n".join(wrapped_chunks)


if __name__ == "__main__":
    pass
