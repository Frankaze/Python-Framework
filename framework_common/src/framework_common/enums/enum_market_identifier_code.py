"""Shared ISO 10383 market identifier codes."""

from enum import Enum


class EnumMarketIdentifierCode(Enum):
    """Identify supported markets using ISO 10383 MIC values."""

    # region Constants

    XTAI: str = "XTAI"
    ROCO: str = "ROCO"

    # endregion Constants
