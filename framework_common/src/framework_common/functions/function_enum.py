"""Shared helpers for resolving enumeration members."""

from enum import Enum


def parse_enum_name[TEnum: Enum](typ_enum: type[TEnum], str_value: str) -> TEnum | None:
    """Resolve an uppercase member name without trimming the supplied text.

    Lookup uses member names, not their values. Unknown names return None.
    """
    return typ_enum.__members__.get(str_value.upper())
