"""Shared string helpers and validation."""

import re

from framework_common.errors.container_error_base import ContainerErrorBase


def validate(
    property_field: property,
    value_actual: object,
    *,
    int_maximum_length: int,
    bol_is_none_allowed: bool,
    bol_is_ascii_only: bool,
    bol_use_utf16: bool,
    bol_require_trimmed: bool,
    typ_container: type[ContainerErrorBase],
) -> None:
    """Validate text while preserving the caller's length and whitespace rules."""
    if value_actual is None and bol_is_none_allowed:
        return
    if not isinstance(value_actual, str):
        raise typ_container.TypeValidationError(
            property_field,
            str,
            type(value_actual),
            bol_is_none_allowed=bol_is_none_allowed,
        )
    if not value_actual.strip():
        raise typ_container.ValueValidationRequiredError(property_field, value_actual)
    _int_length: int = (
        len(value_actual.encode("utf-16-le")) // 2
        if bol_use_utf16
        else len(value_actual)
    )
    if _int_length > int_maximum_length:
        raise typ_container.ValueValidationLengthError(
            property_field,
            value_actual,
            1,
            int_maximum_length,
            _int_length,
            "utf-16-code-units" if bol_use_utf16 else "characters",
        )
    if bol_is_ascii_only and not value_actual.isascii():
        raise typ_container.ValueValidationCharacterSetError(
            property_field, value_actual, "ascii"
        )
    if bol_require_trimmed and value_actual != value_actual.strip():
        raise typ_container.ValueValidationFormatError(
            property_field, value_actual, re.compile(r"\S(?:.*\S)?", re.DOTALL)
        )
