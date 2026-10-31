"""Structured value validation errors without user-facing text."""

from inspect import Parameter

from framework_common.errors.error_base import ErrorBase


class ValueValidationError(ErrorBase):
    """Describe a value mismatch; callers own validation and response formatting."""

    # region Properties

    @property
    def field(self) -> property | Parameter | tuple[Parameter, ...]:
        return self._field

    @property
    def expected_value(self) -> object:
        return self._value_expected

    @property
    def actual_value(self) -> object:
        return self._value_actual

    # endregion Properties

    # region Constructor & Special Methods

    def __init__(
        self,
        field: property | Parameter | tuple[Parameter, ...],
        value_expected: object,
        value_actual: object,
    ) -> None:
        super().__init__()
        self._field: property | Parameter | tuple[Parameter, ...] = field
        self._value_expected: object = value_expected
        self._value_actual: object = value_actual

    # endregion Constructor & Special Methods


class ValueValidationRequiredError(ValueValidationError):
    """Carry structured facts for ValueValidationRequiredError."""

    # region Constructor & Special Methods

    def __init__(
        self,
        field: property | Parameter | tuple[Parameter, ...],
        value_actual: object,
    ) -> None:
        super().__init__(field, None, value_actual)

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
        field: property | Parameter | tuple[Parameter, ...],
        value_actual: object,
        int_minimum_length: int,
        int_maximum_length: int | None,
        int_actual_length: int,
        str_length_unit: str,
    ) -> None:
        super().__init__(field, (int_minimum_length, int_maximum_length), value_actual)
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
        return self._minimum

    @property
    def maximum(self) -> int | float | None:
        return self._maximum

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
        field: property | Parameter | tuple[Parameter, ...],
        value_actual: object,
        minimum: int | float | None,
        maximum: int | float | None,
        bol_is_minimum_inclusive: bool,
        bol_is_maximum_inclusive: bool,
        bol_is_finite_required: bool,
    ) -> None:
        super().__init__(field, (minimum, maximum), value_actual)
        self._minimum: int | float | None = minimum
        self._maximum: int | float | None = maximum
        self._bol_is_minimum_inclusive: bool = bol_is_minimum_inclusive
        self._bol_is_maximum_inclusive: bool = bol_is_maximum_inclusive
        self._bol_is_finite_required: bool = bol_is_finite_required

    # endregion Constructor & Special Methods


class ValueValidationFormatError(ValueValidationError):
    """Carry structured facts for ValueValidationFormatError."""

    # region Properties

    @property
    def expected_format(self) -> object:
        return self._value_expected_format

    # endregion Properties

    # region Constructor & Special Methods

    def __init__(
        self,
        field: property | Parameter | tuple[Parameter, ...],
        value_actual: object,
        value_expected_format: object,
    ) -> None:
        super().__init__(field, value_expected_format, value_actual)
        self._value_expected_format: object = value_expected_format

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
        field: property | Parameter | tuple[Parameter, ...],
        value_actual: object,
        str_character_set: str,
    ) -> None:
        super().__init__(field, str_character_set, value_actual)
        self._str_character_set: str = str_character_set

    # endregion Constructor & Special Methods


class ValueValidationNotAllowedError(ValueValidationError):
    """Carry structured facts for ValueValidationNotAllowedError."""

    # region Properties

    @property
    def allowed_values(self) -> tuple[object, ...]:
        return self._tuple_allowed_values

    # endregion Properties

    # region Constructor & Special Methods

    def __init__(
        self,
        field: property | Parameter | tuple[Parameter, ...],
        value_actual: object,
        tuple_allowed_values: tuple[object, ...],
    ) -> None:
        super().__init__(field, tuple_allowed_values, value_actual)
        self._tuple_allowed_values: tuple[object, ...] = tuple_allowed_values

    # endregion Constructor & Special Methods


class ValueValidationExactlyOneRequiredError(ValueValidationError):
    """Carry a parameter group's presence flags when exactly one must be set."""

    # region Constructor & Special Methods

    def __init__(
        self,
        field: tuple[Parameter, ...],
        value_actual: tuple[bool, ...],
    ) -> None:
        super().__init__(field, 1, value_actual)

    # endregion Constructor & Special Methods


class ValueValidationMustDifferError(ValueValidationError):
    """Carry structured facts for ValueValidationMustDifferError."""

    # region Properties

    @property
    def other_field(self) -> property | Parameter | tuple[Parameter, ...]:
        return self._other_field

    @property
    def other_value(self) -> object:
        return self._value_other

    # endregion Properties

    # region Constructor & Special Methods

    def __init__(
        self,
        field: property | Parameter | tuple[Parameter, ...],
        value_actual: object,
        other_field: property | Parameter | tuple[Parameter, ...],
        value_other: object,
    ) -> None:
        super().__init__(field, value_other, value_actual)
        self._other_field: property | Parameter | tuple[Parameter, ...] = other_field
        self._value_other: object = value_other

    # endregion Constructor & Special Methods
