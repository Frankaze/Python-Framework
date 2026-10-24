"""Track update operands separately from their requested operations."""

from collections.abc import Mapping
from types import MappingProxyType

from framework_common.enums.enum_update_operation import EnumUpdateOperation
from framework_common.errors.standalones.validation.type_validation_error import (
    TypeValidationError,
)
from framework_common.errors.standalones.validation.value_validation_error import (
    ValueValidationLengthError,
    ValueValidationNotAllowedError,
)
from framework_service.models.dm_assigned_base import DmAssignedBase


class DmUpdateBase(DmAssignedBase):
    """Keep plain getters while accepting values or (value, operation) tuples."""

    # region Properties

    @property
    def update_operations(self) -> Mapping[str, EnumUpdateOperation]:
        return MappingProxyType(dict(self._dic_enm_update_operations))

    # endregion Properties

    # region Constructor & Special Methods

    def __init__(self) -> None:
        super().__init__()
        self._dic_enm_update_operations: dict[str, EnumUpdateOperation] = {}

    # endregion Constructor & Special Methods

    # region Internal Methods

    def _parse_update_value[TValue](
        self,
        property_field: property,
        obj_value: TValue | tuple[TValue, EnumUpdateOperation],
        *,
        tpl_allowed_operations: tuple[EnumUpdateOperation, ...] = (
            EnumUpdateOperation.ASSIGN,
        ),
    ) -> TValue:
        """Validate the operation before tracking an assignment; last write wins."""
        _enm_operation: EnumUpdateOperation = EnumUpdateOperation.ASSIGN
        _obj_operand: TValue
        if isinstance(obj_value, tuple):
            if len(obj_value) != 2:
                raise ValueValidationLengthError(
                    property_field,
                    obj_value,
                    int_minimum_length=2,
                    int_maximum_length=2,
                    int_actual_length=len(obj_value),
                    str_length_unit="items",
                )
            _obj_operand, _enm_operation = obj_value
            if not isinstance(_enm_operation, EnumUpdateOperation):
                raise TypeValidationError(
                    property_field,
                    EnumUpdateOperation,
                    type(_enm_operation),
                    bol_is_none_allowed=False,
                )
        else:
            _obj_operand = obj_value
        if _enm_operation not in tpl_allowed_operations:
            raise ValueValidationNotAllowedError(
                property_field,
                _enm_operation,
                tpl_allowed_values=tpl_allowed_operations,
            )
        if _obj_operand is None and _enm_operation is not EnumUpdateOperation.ASSIGN:
            raise ValueValidationNotAllowedError(
                property_field,
                None,
                tpl_allowed_values=(EnumUpdateOperation.ASSIGN,),
            )
        _str_field: str = property_field.fget.__name__
        self._dic_enm_update_operations[_str_field] = _enm_operation
        self._set_str_assigned_fields.add(_str_field)
        return _obj_operand

    # endregion Internal Methods
