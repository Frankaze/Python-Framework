"""Structured function contract errors without response text."""

from types import FunctionType

from framework_common.errors.error_base import ErrorBase


class FunctionValidationError(ErrorBase):
    """Identify the class responsible for a method and its function object."""

    # region Properties

    @property
    def owner_type(self) -> type[object]:
        return self._typ_owner

    @property
    def method(self) -> FunctionType:
        return self._fnc_method

    # endregion Properties

    # region Constructor & Special Methods

    def __init__(self, typ_owner: type[object], fnc_method: FunctionType) -> None:
        super().__init__()
        self._typ_owner: type[object] = typ_owner
        self._fnc_method: FunctionType = fnc_method

    # endregion Constructor & Special Methods


class FunctionValidationNotImplementedError(FunctionValidationError):
    """Report a method contract whose implementation has not been supplied."""
