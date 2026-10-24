"""Structured value validation errors without user-facing text."""

from inspect import Parameter

from framework_common.errors.error_base import ErrorBase


class ValueValidationError(ErrorBase):
    """Describe a value mismatch; callers own validation and response formatting."""

    # region Properties

    @property
    def field(self) -> property | Parameter | tuple[Parameter, ...]:
        return self._obj_field

    @property
    def expected_value(self) -> object:
        return self._obj_expected

    @property
    def actual_value(self) -> object:
        return self._obj_actual

    # endregion Properties

    # region Constructor & Special Methods

    def __init__(
        self,
        obj_field: property | Parameter | tuple[Parameter, ...],
        obj_expected: object,
        obj_actual: object,
    ) -> None:
        super().__init__()
        self._obj_field: property | Parameter | tuple[Parameter, ...] = obj_field
        self._obj_expected: object = obj_expected
        self._obj_actual: object = obj_actual

    # endregion Constructor & Special Methods


class ValueValidationRequiredError(ValueValidationError):
    """Carry structured facts for ValueValidationRequiredError."""

    # region Constructor & Special Methods

    def __init__(
        self,
        obj_field: property | Parameter | tuple[Parameter, ...],
        obj_actual: object,
    ) -> None:
        super().__init__(obj_field, None, obj_actual)

    # endregion Constructor & Special Methods


class ValueValidationLengthError(ValueValidationError):
    """Carry structured facts for ValueValidationLengthError."""

    # region Properties

    @property
    def minimum_length(self) -> int:
        return self._int_minimum_length

    @property
    def maximum_length(self) -> int | None:
        return self._int_maximum_length

    @property
    def actual_length(self) -> int:
        return self._int_actual_length

    @property
    def length_unit(self) -> str:
        return self._str_length_unit

    # endregion Properties

    # region Constructor & Special Methods

    def __init__(
        self,
        obj_field: property | Parameter | tuple[Parameter, ...],
        obj_actual: object,
        int_minimum_length: int,
        int_maximum_length: int | None,
        int_actual_length: int,
        str_length_unit: str,
    ) -> None:
        super().__init__(
            obj_field,
            (int_minimum_length, int_maximum_length),
            obj_actual,
        )
        self._int_minimum_length: int = int_minimum_length
        self._int_maximum_length: int | None = int_maximum_length
        self._int_actual_length: int = int_actual_length
        self._str_length_unit: str = str_length_unit

    # endregion Constructor & Special Methods


class ValueValidationRangeError(ValueValidationError):
    """Carry structured facts for ValueValidationRangeError."""

    # region Properties

    @property
    def minimum(self) -> int | float | None:
        return self._number_minimum

    @property
    def maximum(self) -> int | float | None:
        return self._number_maximum

    @property
    def is_minimum_inclusive(self) -> bool:
        return self._bol_is_minimum_inclusive

    @property
    def is_maximum_inclusive(self) -> bool:
        return self._bol_is_maximum_inclusive

    @property
    def is_finite_required(self) -> bool:
        return self._bol_is_finite_required

    # endregion Properties

    # region Constructor & Special Methods

    def __init__(
        self,
        obj_field: property | Parameter | tuple[Parameter, ...],
        obj_actual: object,
        flt_minimum: float | None,
        flt_maximum: float | None,
        bol_is_minimum_inclusive: bool,
        bol_is_maximum_inclusive: bool,
        bol_is_finite_required: bool,
    ) -> None:
        super().__init__(
            obj_field,
            (flt_minimum, flt_maximum),
            obj_actual,
        )
        self._number_minimum: int | float | None = flt_minimum
        self._number_maximum: int | float | None = flt_maximum
        self._bol_is_minimum_inclusive: bool = bol_is_minimum_inclusive
        self._bol_is_maximum_inclusive: bool = bol_is_maximum_inclusive
        self._bol_is_finite_required: bool = bol_is_finite_required

    # endregion Constructor & Special Methods


class ValueValidationFormatError(ValueValidationError):
    """Carry structured facts for ValueValidationFormatError."""

    # region Properties

    @property
    def expected_format(self) -> object:
        return self._obj_expected_format

    # endregion Properties

    # region Constructor & Special Methods

    def __init__(
        self,
        obj_field: property | Parameter | tuple[Parameter, ...],
        obj_actual: object,
        obj_expected_format: object,
    ) -> None:
        super().__init__(obj_field, obj_expected_format, obj_actual)
        self._obj_expected_format: object = obj_expected_format

    # endregion Constructor & Special Methods


class ValueValidationCharacterSetError(ValueValidationError):
    """Carry structured facts for ValueValidationCharacterSetError."""

    # region Properties

    @property
    def character_set(self) -> str:
        return self._str_character_set

    # endregion Properties

    # region Constructor & Special Methods

    def __init__(
        self,
        obj_field: property | Parameter | tuple[Parameter, ...],
        obj_actual: object,
        str_character_set: str,
    ) -> None:
        super().__init__(obj_field, str_character_set, obj_actual)
        self._str_character_set: str = str_character_set

    # endregion Constructor & Special Methods


class ValueValidationNotAllowedError(ValueValidationError):
    """Carry structured facts for ValueValidationNotAllowedError."""

    # region Properties

    @property
    def allowed_values(self) -> tuple[object, ...]:
        return self._tpl_allowed_values

    # endregion Properties

    # region Constructor & Special Methods

    def __init__(
        self,
        obj_field: property | Parameter | tuple[Parameter, ...],
        obj_actual: object,
        tpl_allowed_values: tuple[object, ...],
    ) -> None:
        super().__init__(obj_field, tpl_allowed_values, obj_actual)
        self._tpl_allowed_values: tuple[object, ...] = tpl_allowed_values

    # endregion Constructor & Special Methods


class ValueValidationExactlyOneRequiredError(ValueValidationError):
    """Carry a parameter group's presence flags when exactly one must be set."""

    # region Constructor & Special Methods

    def __init__(
        self,
        tpl_fields: tuple[Parameter, ...],
        tpl_actual: tuple[bool, ...],
    ) -> None:
        super().__init__(tpl_fields, 1, tpl_actual)

    # endregion Constructor & Special Methods


class ValueValidationMustDifferError(ValueValidationError):
    """Carry structured facts for ValueValidationMustDifferError."""

    # region Properties

    @property
    def other_field(self) -> property | Parameter | tuple[Parameter, ...]:
        return self._obj_other_field

    @property
    def other_value(self) -> object:
        return self._obj_other

    # endregion Properties

    # region Constructor & Special Methods

    def __init__(
        self,
        obj_field: property | Parameter | tuple[Parameter, ...],
        obj_actual: object,
        obj_other_field: property | Parameter | tuple[Parameter, ...],
        obj_other: object,
    ) -> None:
        super().__init__(obj_field, obj_other, obj_actual)
        self._obj_other_field: property | Parameter | tuple[Parameter, ...] = (
            obj_other_field
        )
        self._obj_other: object = obj_other

    # endregion Constructor & Special Methods
