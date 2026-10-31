"""Report a value whose runtime type violates an application's contract."""

from inspect import Parameter

from framework_common.errors.error_base import ErrorBase


class TypeValidationError(ErrorBase):
    """Carry a type mismatch and its nullability rule without user-facing text.

    The field is a Python property descriptor or inspect.Parameter, not a copied name.
    Type fields
    contain class objects, not names or values. Pass type(None)
    as the actual type for None; is_none_allowed describes the expected rule.
    This error carries validation results and does not perform validation.
    """

    # region Properties

    @property
    def field(self) -> property | Parameter:
        return self._field

    @property
    def expected_type(self) -> type[object]:
        return self._typ_expected_type

    @property
    def actual_type(self) -> type[object]:
        return self._typ_actual_type

    @property
    def is_none_allowed(self) -> bool:
        return self._bol_is_none_allowed

    # endregion Properties

    # region Constructor & Special Methods

    def __init__(
        self,
        field: property | Parameter,
        typ_expected_type: type[object],
        typ_actual_type: type[object],
        *,
        bol_is_none_allowed: bool,
    ) -> None:
        super().__init__()
        self._field: property | Parameter = field
        self._typ_expected_type: type[object] = typ_expected_type
        self._typ_actual_type: type[object] = typ_actual_type
        self._bol_is_none_allowed: bool = bol_is_none_allowed

    # endregion Constructor & Special Methods
