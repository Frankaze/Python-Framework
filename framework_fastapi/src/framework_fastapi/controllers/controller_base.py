"""Shared foundation for lightweight API controllers."""

from framework_utility.logger_mixin import LoggerMixin


class ControllerBase(LoggerMixin):
    """Base for lightweight controllers that route requests to API models."""
