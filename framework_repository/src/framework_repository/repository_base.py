"""Shared entity operations and dynamic queries without transaction ownership."""

from inspect import signature
from typing import Any

from sqlalchemy import Select, select
from sqlalchemy.orm import Session
from sqlalchemy.orm.interfaces import ORMOption
from sqlalchemy.sql.elements import ColumnElement

from framework_common.errors.standalones.validation import ValueValidationRangeError
from framework_repository.entity_base import EntityBase


class RepositoryBase[TEntity: EntityBase]:
    """Access mapped entities using a Session owned by the unit of work."""

    # region Constructor & Special Methods

    def __init__(
        self,
        sqls: Session,
        typ_entity: type[TEntity],
    ) -> None:
        self._sqls: Session = sqls
        self._typ_entity: type[TEntity] = typ_entity

    # endregion Constructor & Special Methods

    # region Public Methods

    def get_many(
        self,
        lst_col_conditions: list[ColumnElement[bool]] | None = None,
        lst_col_order: list[ColumnElement[Any]] | None = None,
        int_limit: int | None = None,
        *,
        lst_ormo_options: list[ORMOption] | None = None,
    ) -> list[TEntity]:
        """Return matching entities with optional AND conditions and ordering.

        Missing or empty conditions select all entities. No limit means all
        matches; zero returns no entities, and negative limits are invalid.
        Order expressions may contain columns with different value types.
        """
        if int_limit is not None and int_limit < 0:
            raise ValueValidationRangeError(
                field=signature(RepositoryBase.get_many).parameters["int_limit"],
                value_actual=int_limit,
                minimum=0,
                maximum=None,
                bol_is_minimum_inclusive=True,
                bol_is_maximum_inclusive=True,
                bol_is_finite_required=False,
            )

        _stmt: Select[tuple[TEntity]] = select(self._typ_entity)
        if lst_ormo_options:
            _stmt = _stmt.options(*lst_ormo_options)
        if lst_col_conditions:
            _stmt = _stmt.where(*lst_col_conditions)
        if lst_col_order:
            _stmt = _stmt.order_by(*lst_col_order)
        if int_limit is not None:
            _stmt = _stmt.limit(int_limit)
        return list(self._sqls.scalars(_stmt).unique().all())

    def get_first(
        self,
        lst_col_conditions: list[ColumnElement[bool]] | None = None,
        lst_col_order: list[ColumnElement[Any]] | None = None,
        *,
        lst_ormo_options: list[ORMOption] | None = None,
    ) -> TEntity | None:
        """Return the first match or None, requesting at most one row.

        Missing or empty conditions select from all entities. Supply ordering
        to define the first row.
        """
        _stmt: Select[tuple[TEntity]] = select(self._typ_entity)
        if lst_ormo_options:
            _stmt = _stmt.options(*lst_ormo_options)
        if lst_col_conditions:
            _stmt = _stmt.where(*lst_col_conditions)
        if lst_col_order:
            _stmt = _stmt.order_by(*lst_col_order)
        _stmt = _stmt.limit(1)
        return self._sqls.scalars(_stmt).unique().first()

    def add(self, ent_entity: TEntity) -> None:
        self._sqls.add(ent_entity)

    def delete(self, ent_entity: TEntity) -> None:
        self._sqls.delete(ent_entity)

    # endregion Public Methods
