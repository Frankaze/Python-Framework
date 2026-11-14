"""Shared timeframe units for time-based data."""

from enum import Enum


class EnumTimeframe(Enum):
    """Identify a single timeframe unit without abbreviations or multipliers."""

    # region Constants

    SECOND: str = "Second"
    MINUTE: str = "Minute"
    HOUR: str = "Hour"
    DAY: str = "Day"
    WEEK: str = "Week"
    MONTH: str = "Month"
    QUARTER: str = "Quarter"
    YEAR: str = "Year"

    # endregion Constants
