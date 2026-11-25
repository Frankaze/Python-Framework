"""Shared logging levels for application configuration."""

from enum import Enum


class EnumLogLevel(Enum):
    """Name the standard library logging levels; values are logging level names."""

    # region Constants

    DEBUG: str = "DEBUG"
    INFO: str = "INFO"
    WARNING: str = "WARNING"
    ERROR: str = "ERROR"
    CRITICAL: str = "CRITICAL"

    # endregion Constants
