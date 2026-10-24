"""Shared configuration for all website-specific sources."""


class SourceBase:
    """Store connection settings shared by source implementations."""

    # region Properties

    @property
    def timeout(self) -> float:
        return self._flt_timeout

    @property
    def request_interval(self) -> float:
        return self._flt_request_interval

    # endregion Properties

    # region Constructor & Special Methods

    def __init__(
        self,
        flt_timeout: float = 30.0,
        flt_request_interval: float = 1.0,
    ) -> None:
        self._flt_timeout: float = flt_timeout
        self._flt_request_interval: float = flt_request_interval

    # endregion Constructor & Special Methods
