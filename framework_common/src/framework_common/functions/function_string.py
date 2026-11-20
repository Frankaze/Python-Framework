"""Shared string helpers and validation."""

import re

from framework_common.errors.container_error_base import ContainerErrorBase


def validate(
    property_field: property,
    obj_actual: object,
    *,
    int_maximum_length: int,
    bol_is_none_allowed: bool,
    bol_is_ascii_only: bool,
    bol_use_utf16: bool,
    bol_require_trimmed: bool,
    typ_container: type[ContainerErrorBase],
) -> None:
    """Validate text while preserving the caller's length and whitespace rules."""
    if obj_actual is None and bol_is_none_allowed:
        return
    if not isinstance(obj_actual, str):
        raise typ_container.TypeValidationError(
            property_field,
            str,
            type(obj_actual),
            bol_is_none_allowed=bol_is_none_allowed,
        )
    _str_actual: str = obj_actual
    if not _str_actual.strip():
        raise typ_container.ValueValidationRequiredError(property_field, _str_actual)
    _int_length: int = (
        len(_str_actual.encode("utf-16-le")) // 2 if bol_use_utf16 else len(_str_actual)
    )
    if _int_length > int_maximum_length:
        raise typ_container.ValueValidationLengthError(
            property_field,
            _str_actual,
            1,
            int_maximum_length,
            _int_length,
            "utf-16-code-units" if bol_use_utf16 else "characters",
        )
    if bol_is_ascii_only and not _str_actual.isascii():
        raise typ_container.ValueValidationCharacterSetError(
            property_field, _str_actual, "ascii"
        )
    if bol_require_trimmed and _str_actual != _str_actual.strip():
        raise typ_container.ValueValidationFormatError(
            property_field, _str_actual, re.compile(r"\S(?:.*\S)?", re.DOTALL)
        )
