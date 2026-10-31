"""Structured errors for validation."""

from framework_common.errors.standalones.validation.function_validation_error import (
    FunctionValidationError,
    FunctionValidationNotImplementedError,
)
from framework_common.errors.standalones.validation.mapper_validation_error import (
    MapperValidationError,
    MapperValidationResultEmptyError,
)
from framework_common.errors.standalones.validation.type_validation_error import (
    TypeValidationError,
)
from framework_common.errors.standalones.validation.value_validation_error import (
    ValueValidationCharacterSetError,
    ValueValidationError,
    ValueValidationExactlyOneRequiredError,
    ValueValidationFormatError,
    ValueValidationLengthError,
    ValueValidationMustDifferError,
    ValueValidationNotAllowedError,
    ValueValidationRangeError,
    ValueValidationRequiredError,
)

__all__: list[str] = [
    "FunctionValidationError",
    "FunctionValidationNotImplementedError",
    "MapperValidationError",
    "MapperValidationResultEmptyError",
    "TypeValidationError",
    "ValueValidationError",
    "ValueValidationExactlyOneRequiredError",
    "ValueValidationRequiredError",
    "ValueValidationLengthError",
    "ValueValidationRangeError",
    "ValueValidationFormatError",
    "ValueValidationCharacterSetError",
    "ValueValidationNotAllowedError",
    "ValueValidationMustDifferError",
]
