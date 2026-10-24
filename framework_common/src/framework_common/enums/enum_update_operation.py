"""Shared operation identifiers for partial updates."""

from enum import Enum


class EnumUpdateOperation(Enum):
    """Identify value assignment, numeric increment, or text append intent."""

    # region Constants

    ASSIGN: str = "Assign"
    INCREMENT: str = "Increment"
    APPEND: str = "Append"

    # endregion Constants
