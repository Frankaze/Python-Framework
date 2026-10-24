"""Shared trigger types for application job executions."""

from enum import Enum


class EnumJobTriggerType(Enum):
    """Identify how a job execution was triggered."""

    # region Constants

    SCHEDULED: str = "Scheduled"
    MANUAL: str = "Manual"

    # endregion Constants
