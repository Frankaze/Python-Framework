"""Shared integer helpers and validation."""

from framework_common.errors.container_error_base import ContainerErrorBase


def validate(
    property_field: property,
    value_actual: object,
    *,
    int_minimum: int,
    int_maximum: int,
    bol_is_none_allowed: bool,
    typ_container: type[ContainerErrorBase],
) -> None:
    """Check an exact int type, excluding bool, then validate inclusive bounds."""
    if value_actual is None and bol_is_none_allowed:
        return
    if type(value_actual) is not int:
        raise typ_container.TypeValidationError(
            property_field,
            int,
            type(value_actual),
            bol_is_none_allowed=bol_is_none_allowed,
        )
    if not int_minimum <= value_actual <= int_maximum:
        raise typ_container.ValueValidationRangeError(
            property_field, value_actual, int_minimum, int_maximum, True, True, True
        )
