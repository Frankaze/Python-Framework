"""Calendar months and their numeric values."""

from enum import Enum


class EnumMonth(Enum):
    """Map English month names to calendar month numbers."""

    # region Constants

    JANUARY: int = 1
    FEBRUARY: int = 2
    MARCH: int = 3
    APRIL: int = 4
    MAY: int = 5
    JUNE: int = 6
    JULY: int = 7
    AUGUST: int = 8
    SEPTEMBER: int = 9
    OCTOBER: int = 10
    NOVEMBER: int = 11
    DECEMBER: int = 12

    # endregion Constants
