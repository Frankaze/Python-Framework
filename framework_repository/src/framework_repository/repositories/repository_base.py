"""Shared entity operations and dynamic queries without transaction ownership."""

from collections.abc import Mapping
from decimal import Decimal
from inspect import signature
from math import isfinite
from typing import Any

from sqlalchemy import Float, Integer, Numeric, Select, String, literal, select
from sqlalchemy import inspect as inspect_entity
from sqlalchemy.orm import Session
from sqlalchemy.orm.interfaces import ORMOption
from sqlalchemy.sql.elements import ColumnElement

from framework_common.enums.enum_update_operation import EnumUpdateOperation
from framework_common.errors.standalones.validation.value_validation_error import (
    ValueValidationNotAllowedError,
    ValueValidationRangeError,
)
from framework_repository.models.entity_base import EntityBase
from framework_utility.logger_mixin import LoggerMixin


class RepositoryBase[TEntity: EntityBase](LoggerMixin):
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
                obj_field=signature(RepositoryBase.get_many).parameters["int_limit"],
                obj_actual=int_limit,
                flt_minimum=0,
                flt_maximum=None,
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

    def apply_update(
        self,
        ent_entity: TEntity,
        dic_values: Mapping[str, object],
        dic_enm_operations: Mapping[str, EnumUpdateOperation] | None = None,
    ) -> bool:
        """Stage assignments or SQL expressions without flushing or committing.

        Numeric increments and text appends reference the database column, so
        they do not overwrite a concurrently changed value with a Python sum.
        NULL stays NULL. Return whether any local changes were staged.
        """
        _dic_enm_operations: Mapping[str, EnumUpdateOperation] = (
            dic_enm_operations if dic_enm_operations is not None else {}
        )
        _set_str_unknown: set[str] = set(_dic_enm_operations) - set(dic_values)
        if _set_str_unknown:
            raise ValueValidationNotAllowedError(
                signature(RepositoryBase.apply_update).parameters["dic_enm_operations"],
                min(_set_str_unknown),
                tpl_allowed_values=tuple(sorted(dic_values)),
            )
        _dic_changes: dict[str, object] = {}
        _str_field: str
        _obj_value: object
        for _str_field, _obj_value in dic_values.items():
            _enm_operation: EnumUpdateOperation = _dic_enm_operations.get(
                _str_field, EnumUpdateOperation.ASSIGN
            )
            if not isinstance(_enm_operation, EnumUpdateOperation):
                raise ValueValidationNotAllowedError(
                    signature(RepositoryBase.apply_update).parameters[
                        "dic_enm_operations"
                    ],
                    _enm_operation,
                    tpl_allowed_values=tuple(EnumUpdateOperation),
                )
            if _enm_operation is EnumUpdateOperation.ASSIGN:
                _obj_current: object = getattr(ent_entity, _str_field)
                if (
                    isinstance(_obj_current, ColumnElement)
                    or _obj_current != _obj_value
                ):
                    _dic_changes[_str_field] = _obj_value
                continue
            _col_field: ColumnElement[Any] = getattr(
                self._typ_entity, _str_field
            ).__clause_element__()
            _bol_numeric: bool = (
                type(_obj_value) in (int, float, Decimal)
                and isinstance(_col_field.type, (Integer, Numeric, Float))
                and (
                    _obj_value.is_finite()
                    if isinstance(_obj_value, Decimal)
                    else isfinite(_obj_value)
                    if isinstance(_obj_value, float)
                    else True
                )
            )
            if (
                _enm_operation is EnumUpdateOperation.INCREMENT and not _bol_numeric
            ) or (
                _enm_operation is EnumUpdateOperation.APPEND
                and not (
                    isinstance(_col_field.type, String) and isinstance(_obj_value, str)
                )
            ):
                raise ValueValidationNotAllowedError(
                    signature(RepositoryBase.apply_update).parameters["dic_values"],
                    (_str_field, _obj_value, _enm_operation),
                    tpl_allowed_values=(EnumUpdateOperation.ASSIGN,),
                )
            _obj_current = getattr(ent_entity, _str_field)
            if (
                _enm_operation is EnumUpdateOperation.INCREMENT and _obj_value == 0
            ) or (_enm_operation is EnumUpdateOperation.APPEND and _obj_value == ""):
                continue
            # Preserve earlier pending changes to this field in the same UoW.
            _col_base: ColumnElement[Any] = _col_field
            if isinstance(_obj_current, ColumnElement):
                _col_base = _obj_current
            elif inspect_entity(ent_entity).attrs[_str_field].history.has_changes():
                _col_base = literal(_obj_current, type_=_col_field.type)
            _dic_changes[_str_field] = (
                _col_base + _obj_value
                if _enm_operation is EnumUpdateOperation.INCREMENT
                else _col_base.concat(_obj_value)
            )
        # Validate every operand before changing any field of the entity.
        for _str_field, _obj_value in _dic_changes.items():
            setattr(ent_entity, _str_field, _obj_value)
        return bool(_dic_changes)

    def delete(self, ent_entity: TEntity) -> None:
        self._sqls.delete(ent_entity)

    # endregion Public Methods
