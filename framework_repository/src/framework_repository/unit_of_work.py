"""Database transaction ownership for services sharing one SQLAlchemy Session."""

from __future__ import annotations

from collections.abc import Callable
from types import FunctionType, TracebackType
from typing import Self

from sqlalchemy.orm import Session

from framework_common.errors.containers import PersistenceError


class UnitOfWork:
    """Explicit commits; only the root owns commit, rollback and close.

    Use a fresh root for each business operation. A child shares its Session
    and can flush. A child never commits or closes the shared Session.
    Its commit() still raises when the shared state requires rollback.
    Leaving a root context rolls back any unsaved changes and closes it.
    """

    # region Properties

    @property
    def is_sub_unit(self) -> bool:
        return self._bol_is_sub_unit

    @property
    def session(self) -> Session:
        self._ensure_open(UnitOfWork.session.fget)
        if self._sst_state.session is None:
            self._sst_state.session = self._sst_state.session_factory()
        return self._sst_state.session

    # endregion Properties

    # region Constructor & Special Methods

    def __init__(self, fnc_session_factory: Callable[[], Session]) -> None:
        self._sst_state: UnitOfWork._SessionState = UnitOfWork._SessionState(
            fnc_session_factory
        )
        self._bol_is_sub_unit: bool = False
        self._bol_entered: bool = False

    def __enter__(self) -> Self:
        self._ensure_open(UnitOfWork.__enter__)
        if self._bol_entered:
            raise PersistenceError.AlreadyActiveError()
        self._bol_entered = True
        return self

    def __exit__(
        self,
        typ_exception: type[BaseException] | None,
        exc_exception: BaseException | None,
        trb_traceback: TracebackType | None,
    ) -> None:
        self._bol_entered = False
        if typ_exception is not None:
            self._sst_state.is_rollback_only = True
        if not self._bol_is_sub_unit:
            try:
                if not self._sst_state.is_closed:
                    self.rollback()
            finally:
                self.close()

    # endregion Constructor & Special Methods

    # region Public Methods

    def create_sub_unit(self) -> UnitOfWork:
        self._ensure_open(UnitOfWork.create_sub_unit)
        _uow_child: UnitOfWork = UnitOfWork(self._sst_state.session_factory)
        _uow_child._sst_state = self._sst_state
        _uow_child._bol_is_sub_unit = True
        return _uow_child

    def commit(self) -> None:
        """Commit all shared changes on the root; never commit on a child."""
        self._ensure_open(UnitOfWork.commit)
        if self._sst_state.is_rollback_only:
            raise PersistenceError.TransactionMarkedForRollbackError(
                fnc_method=UnitOfWork.commit
            )
        if self._bol_is_sub_unit:
            return
        try:
            self.session.commit()
        except BaseException:
            self._sst_state.is_rollback_only = True
            raise

    def flush(self) -> None:
        """Send pending SQL (e.g. to obtain generated IDs) without committing."""
        self._ensure_open(UnitOfWork.flush)
        if self._sst_state.is_rollback_only:
            raise PersistenceError.TransactionMarkedForRollbackError(
                fnc_method=UnitOfWork.flush
            )
        try:
            self.session.flush()
        except BaseException:
            self._sst_state.is_rollback_only = True
            raise

    def rollback(self) -> None:
        """Roll back on the root; on a child, mark rollback-only and raise."""
        self._ensure_open(UnitOfWork.rollback)
        if self._bol_is_sub_unit:
            self._sst_state.is_rollback_only = True
            raise PersistenceError.TransactionRollbackRequestedError()
        if self._sst_state.session is not None:
            self._sst_state.session.rollback()
        self._sst_state.is_rollback_only = False

    def close(self) -> None:
        """Release the root Session; closing a child does not release it."""
        if self._bol_is_sub_unit or self._sst_state.is_closed:
            return
        try:
            if self._sst_state.session is not None:
                self._sst_state.session.close()
        finally:
            self._sst_state.is_closed = True

    # endregion Public Methods

    # region Internal Methods

    def _ensure_open(self, fnc_method: FunctionType) -> None:
        if self._sst_state.is_closed:
            raise PersistenceError.ClosedError(fnc_method=fnc_method)

    # endregion Internal Methods

    # region Nested Classes

    class _SessionState:
        """Shared Session and transaction state for a root and its children."""

        # region Properties

        @property
        def session_factory(self) -> Callable[[], Session]:
            return self._fnc_session_factory

        @property
        def session(self) -> Session | None:
            return self._sqls_session

        @session.setter
        def session(self, sqls_session: Session | None) -> None:
            self._sqls_session = sqls_session

        @property
        def is_rollback_only(self) -> bool:
            return self._bol_is_rollback_only

        @is_rollback_only.setter
        def is_rollback_only(self, bol_is_rollback_only: bool) -> None:
            self._bol_is_rollback_only = bol_is_rollback_only

        @property
        def is_closed(self) -> bool:
            return self._bol_is_closed

        @is_closed.setter
        def is_closed(self, bol_is_closed: bool) -> None:
            self._bol_is_closed = bol_is_closed

        # endregion Properties

        # region Constructor & Special Methods

        def __init__(self, fnc_session_factory: Callable[[], Session]) -> None:
            self._fnc_session_factory: Callable[[], Session] = fnc_session_factory
            self._sqls_session: Session | None = None
            self._bol_is_rollback_only: bool = False
            self._bol_is_closed: bool = False

        # endregion Constructor & Special Methods

    # endregion Nested Classes
