This is a python library for breaking and wrapping text.

The library provides three functions, `wrap`, `chunk`, and `break_lines`.

`chunk` breaks a string once, using whitespace, existing hyphens or soft
hyphens, or by forcing a hyphen at a given maximum width, returning the head and
the tail (as a `tuple[str, str]`, with the second slot of the tuple potentially
being an empty string).

`break_lines` breaks a string into lines of a given maximum width, returning
the resulting lines as a `list[str]`.

`wrap` wraps a text.


# Install

    pip install tamal


# Documentation

See [jnthnhrrr.github.io/python-tamal](https://jnthnhrrr.github.io/python-tamal)
