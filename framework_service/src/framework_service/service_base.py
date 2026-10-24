"""Unit of Work construction and lifecycle for application services."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from types import TracebackType
from typing import Self, overload

from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import ColumnElement

from framework_repository import UnitOfWork


class ServiceBase:
    """Create a root UoW or use a supplied UoW, keeping commits explicit.

    Supply exactly one of a Session factory or an existing UoW. Use a fresh
    service context per operation; compose services with child UoWs.
    """

    # region Properties

    @property
    def uow(self) -> UnitOfWork:
        return self._uow

    # endregion Properties

    # region Constructor & Special Methods

    @overload
    def __init__(self, fnc_session_factory: Callable[[], Session]) -> None: ...

    @overload
    def __init__(self, *, uow: UnitOfWork) -> None: ...

    def __init__(
        self,
        fnc_session_factory: Callable[[], Session] | None = None,
        *,
        uow: UnitOfWork | None = None,
    ) -> None:
        if fnc_session_factory is not None and uow is not None:
            raise ValueError("Supply either a Session factory or a UoW, not both.")

        self._uow: UnitOfWork
        if uow is not None:
            self._uow = uow
        elif fnc_session_factory is not None:
            self._uow = UnitOfWork(fnc_session_factory)
        else:
            raise ValueError("A Session factory or a UoW is required.")

    def __enter__(self) -> Self:
        self._uow.__enter__()
        return self

    def __exit__(
        self,
        typ_exception: type[BaseException] | None,
        exc_exception: BaseException | None,
        trb_traceback: TracebackType | None,
    ) -> None:
        self._uow.__exit__(typ_exception, exc_exception, trb_traceback)

    # endregion Constructor & Special Methods

    # region Internal Methods

    def _get_query_conditions[TQuery](
        self,
        dm_query: TQuery | None,
        typ_mapper: type[ServiceBase.MapperBase[TQuery]],
    ) -> list[ColumnElement[bool]]:
        """Validate and map a query using the supplied query-specific mapper."""
        if dm_query is None:
            raise ValueError("A query is required.")
        _lst_col_conditions: list[ColumnElement[bool]] = typ_mapper.to_conditions(
            dm_query
        )
        if not _lst_col_conditions:
            raise ValueError("A query must contain at least one condition.")
        return _lst_col_conditions

    # endregion Internal Methods

    # region Nested Classes

    class MapperBase[TQuery](ABC):
        """Define the query conversion contract for service-specific mappers."""

        # region Public Methods

        @staticmethod
        @abstractmethod
        def to_conditions(dm_query: TQuery) -> list[ColumnElement[bool]]:
            """Convert a query model into predicates without executing queries."""
            raise NotImplementedError("The mapper must implement to_conditions().")

        # endregion Public Methods

    # endregion Nested Classes
