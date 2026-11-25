"""Provide logger access for classes that inherit LoggerMixin."""

import logging


class LoggerMixin:
    """Expose the logger for the concrete subclass's module."""

    # region Properties

    @property
    def _logger(self) -> logging.Logger:
        return logging.getLogger(type(self).__module__)

    # endregion Properties
