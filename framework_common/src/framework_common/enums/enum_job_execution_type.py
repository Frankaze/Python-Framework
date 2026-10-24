"""Shared execution types for application jobs."""

from enum import Enum


class EnumJobExecutionType(Enum):
    """Identify how a job invokes its operation."""

    # region Constants

    API: str = "Api"
    SERVICE: str = "Service"

    # endregion Constants
