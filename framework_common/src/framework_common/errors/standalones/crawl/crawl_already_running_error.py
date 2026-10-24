"""Report a crawl that conflicts with an already running operation."""

from framework_common.errors.error_base import ErrorBase


class CrawlAlreadyRunningError(ErrorBase):
    """Carry the requested crawl target without selecting user-facing text."""

    # region Properties

    @property
    def target(self) -> str:
        return self._str_target

    # endregion Properties

    # region Constructor & Special Methods

    def __init__(self, str_target: str) -> None:
        super().__init__()
        self._str_target: str = str_target

    # endregion Constructor & Special Methods
