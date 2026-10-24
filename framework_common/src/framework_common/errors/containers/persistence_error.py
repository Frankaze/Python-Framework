"""Group persistence lifecycle and transaction errors without response text."""

from types import FunctionType

from framework_common.errors.container_error_base import ContainerErrorBase
from framework_common.errors.error_base import ErrorBase


class PersistenceError(ContainerErrorBase):
    """Group concrete persistence errors without becoming an exception itself."""

    # region Nested Classes

    class AlreadyActiveError(ErrorBase):
        """Report a repeated entry into an active persistence context."""

    class ClosedError(ErrorBase):
        """Identify an operation attempted after its persistence scope closed."""

        # region Properties

        @property
        def method(self) -> FunctionType:
            return self._fnc_method

        # endregion Properties

        # region Constructor & Special Methods

        def __init__(self, fnc_method: FunctionType) -> None:
            super().__init__()
            self._fnc_method: FunctionType = fnc_method

        # endregion Constructor & Special Methods

    class TransactionMarkedForRollbackError(ErrorBase):
        """Identify an operation blocked by the shared rollback-only state."""

        # region Properties

        @property
        def method(self) -> FunctionType:
            return self._fnc_method

        # endregion Properties

        # region Constructor & Special Methods

        def __init__(self, fnc_method: FunctionType) -> None:
            super().__init__()
            self._fnc_method: FunctionType = fnc_method

        # endregion Constructor & Special Methods

    class TransactionRollbackRequestedError(ErrorBase):
        """Propagate a child's request to roll back the shared transaction."""

    # endregion Nested Classes
