"""Unit of Work construction and lifecycle for application services."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from inspect import signature
from types import TracebackType
from typing import Self, overload

from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import ColumnElement

from framework_common.errors.standalones.validation import (
    FunctionValidationNotImplementedError,
    MapperValidationResultEmptyError,
    TypeValidationError,
    ValueValidationExactlyOneRequiredError,
    ValueValidationLengthError,
    ValueValidationRequiredError,
)
from framework_repository import UnitOfWork
from framework_service.dm_assigned_base import DmAssignedBase


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
        _tuple_provided: tuple[bool, bool] = (
            fnc_session_factory is not None,
            uow is not None,
        )
        if sum(_tuple_provided) != 1:
            raise ValueValidationExactlyOneRequiredError(
                field=(
                    signature(ServiceBase.__init__).parameters["fnc_session_factory"],
                    signature(ServiceBase.__init__).parameters["uow"],
                ),
                value_actual=_tuple_provided,
            )

        self._uow: UnitOfWork
        if uow is not None:
            self._uow = uow
        elif fnc_session_factory is not None:
            self._uow = UnitOfWork(fnc_session_factory)

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

    def _get_query_conditions[TQuery: DmAssignedBase](
        self,
        dm_query: TQuery | None,
        typ_mapper: type[ServiceBase.MapperBase[TQuery]],
    ) -> list[ColumnElement[bool]]:
        """Validate and map a query using the supplied query-specific mapper."""
        if dm_query is None:
            raise ValueValidationRequiredError(
                field=signature(ServiceBase._get_query_conditions).parameters[
                    "dm_query"
                ],
                value_actual=dm_query,
            )
        if not isinstance(dm_query, DmAssignedBase):
            raise TypeValidationError(
                field=signature(ServiceBase._get_query_conditions).parameters[
                    "dm_query"
                ],
                typ_expected_type=DmAssignedBase,
                typ_actual_type=type(dm_query),
                bol_is_none_allowed=False,
            )
        if not dm_query.assigned_fields:
            raise ValueValidationLengthError(
                field=DmAssignedBase.assigned_fields,
                value_actual=dm_query.assigned_fields,
                int_minimum_length=1,
                int_maximum_length=None,
                int_actual_length=0,
                str_length_unit="items",
            )
        _lst_col_conditions: list[ColumnElement[bool]] = typ_mapper.to_conditions(
            dm_query
        )
        if not _lst_col_conditions:
            raise MapperValidationResultEmptyError(
                typ_mapper=typ_mapper, fnc_method=typ_mapper.to_conditions
            )
        return _lst_col_conditions

    def _get_update_values[TUpdate: DmAssignedBase](
        self,
        dm_update: TUpdate | None,
        typ_mapper: type[ServiceBase.UpdateMapperBase[TUpdate]],
    ) -> dict[str, object]:
        """Validate and map all update values before accessing an entity."""
        if dm_update is None:
            raise ValueValidationRequiredError(
                field=signature(ServiceBase._get_update_values).parameters["dm_update"],
                value_actual=dm_update,
            )
        if not isinstance(dm_update, DmAssignedBase):
            raise TypeValidationError(
                field=signature(ServiceBase._get_update_values).parameters["dm_update"],
                typ_expected_type=DmAssignedBase,
                typ_actual_type=type(dm_update),
                bol_is_none_allowed=False,
            )
        if not dm_update.assigned_fields:
            raise ValueValidationLengthError(
                field=DmAssignedBase.assigned_fields,
                value_actual=dm_update.assigned_fields,
                int_minimum_length=1,
                int_maximum_length=None,
                int_actual_length=0,
                str_length_unit="items",
            )
        _dic_values: dict[str, object] = typ_mapper.to_update_values(dm_update)
        if not _dic_values:
            raise MapperValidationResultEmptyError(
                typ_mapper=typ_mapper, fnc_method=typ_mapper.to_update_values
            )
        return _dic_values

    def _apply_update[TEntity, TUpdate: DmAssignedBase](
        self,
        ent_entity: TEntity,
        dm_update: TUpdate,
        typ_mapper: type[ServiceBase.UpdateMapperBase[TUpdate]],
    ) -> bool:
        """Apply changed mapped values without owning audit fields or commits."""
        _dic_values: dict[str, object] = self._get_update_values(dm_update, typ_mapper)
        _str_field: str
        _value: object
        _dic_changes: dict[str, object] = {
            _str_field: _value
            for _str_field, _value in _dic_values.items()
            if getattr(ent_entity, _str_field) != _value
        }
        for _str_field, _value in _dic_changes.items():
            setattr(ent_entity, _str_field, _value)
        return bool(_dic_changes)

    # endregion Internal Methods

    # region Nested Classes

    class MapperBase[TQuery: DmAssignedBase](ABC):
        """Define the query conversion contract for service-specific mappers."""

        # region Public Methods

        @classmethod
        @abstractmethod
        def to_conditions(cls, dm_query: TQuery) -> list[ColumnElement[bool]]:
            """Convert a query model into predicates without executing queries."""
            raise FunctionValidationNotImplementedError(
                typ_owner=cls,
                fnc_method=ServiceBase.MapperBase.to_conditions.__func__,
            )

        # endregion Public Methods

    class UpdateMapperBase[TUpdate: DmAssignedBase](ABC):
        """Map explicit updates to validated ORM attribute names and values."""

        # region Public Methods

        @classmethod
        @abstractmethod
        def to_update_values(cls, dm_update: TUpdate) -> dict[str, object]:
            """Validate and convert assigned fields without mutating an entity."""
            raise FunctionValidationNotImplementedError(
                typ_owner=cls,
                fnc_method=ServiceBase.UpdateMapperBase.to_update_values.__func__,
            )

        # endregion Public Methods

    # endregion Nested Classes
