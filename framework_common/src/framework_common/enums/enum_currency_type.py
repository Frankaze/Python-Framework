"""Shared currency types for quote units."""

from enum import Enum


class EnumCurrencyType(Enum):
    """Classify quote units, including venue-specific tokens and points."""

    # region Constants

    FIAT: str = "Fiat"
    CRYPTO: str = "Crypto"
    STABLE: str = "Stable"
    TOKEN: str = "Token"

    # endregion Constants
