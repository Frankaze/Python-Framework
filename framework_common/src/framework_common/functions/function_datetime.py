"""Shared datetime helpers."""

from datetime import UTC, datetime
from typing import overload


@overload
def to_utc_aware(dt_value: datetime) -> datetime: ...


@overload
def to_utc_aware(dt_value: None) -> None: ...


def to_utc_aware(dt_value: datetime | None) -> datetime | None:
    """Mark a stored naive UTC value as UTC so JSON carries the offset.

    Use only for values already known to be UTC, such as TIMESTAMP columns
    stored as naive UTC. Aware values are returned unchanged.
    """
    if dt_value is None or dt_value.tzinfo is not None:
        return dt_value
    return dt_value.replace(tzinfo=UTC)


@overload
def to_utc_naive(dt_value: datetime) -> datetime: ...


@overload
def to_utc_naive(dt_value: None) -> None: ...


def to_utc_naive(dt_value: datetime | None) -> datetime | None:
    """Convert an aware value to naive UTC for storage in a TIMESTAMP column.

    A naive value is rejected: its time zone is unknown, so it cannot be stored
    under the UTC contract.
    """
    if dt_value is None:
        return None
    if dt_value.utcoffset() is None:
        raise ValueError("A timezone-aware datetime is required.")
    return dt_value.astimezone(UTC).replace(tzinfo=None)
