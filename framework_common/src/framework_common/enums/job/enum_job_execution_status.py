"""Shared lifecycle statuses for application job executions."""

from enum import Enum


class EnumJobExecutionStatus(Enum):
    """Describe the state of an individual job execution attempt."""

    # region Constants

    RUNNING: str = "Running"
    SUCCEEDED: str = "Succeeded"
    FAILED: str = "Failed"
    INTERRUPTED: str = "Interrupted"

    # endregion Constants
