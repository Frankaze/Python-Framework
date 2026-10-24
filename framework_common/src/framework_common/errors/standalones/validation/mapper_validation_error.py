"""Structured mapper validation errors without response text."""

from types import FunctionType

from framework_common.errors.error_base import ErrorBase


class MapperValidationError(ErrorBase):
    """Identify the mapper and its method without providing response text."""

    # region Properties

    @property
    def mapper_type(self) -> type[object]:
        return self._typ_mapper

    @property
    def method(self) -> FunctionType:
        return self._fnc_method

    # endregion Properties

    # region Constructor & Special Methods

    def __init__(self, typ_mapper: type[object], fnc_method: FunctionType) -> None:
        super().__init__()
        self._typ_mapper: type[object] = typ_mapper
        self._fnc_method: FunctionType = fnc_method

    # endregion Constructor & Special Methods


class MapperValidationResultEmptyError(MapperValidationError):
    """Report no mapper output for an explicitly assigned input."""
