"""Shared validation error entries for public application error containers."""

from framework_common.errors.standalones.validation import (
    TypeValidationError as _TypeValidationError,
)
from framework_common.errors.standalones.validation import (
    ValueValidationCharacterSetError as _ValueValidationCharacterSetError,
)
from framework_common.errors.standalones.validation import (
    ValueValidationError as _ValueValidationError,
)
from framework_common.errors.standalones.validation import (
    ValueValidationExactlyOneRequiredError as _ValueValidationExactlyOneRequiredError,
)
from framework_common.errors.standalones.validation import (
    ValueValidationFormatError as _ValueValidationFormatError,
)
from framework_common.errors.standalones.validation import (
    ValueValidationLengthError as _ValueValidationLengthError,
)
from framework_common.errors.standalones.validation import (
    ValueValidationMustDifferError as _ValueValidationMustDifferError,
)
from framework_common.errors.standalones.validation import (
    ValueValidationNotAllowedError as _ValueValidationNotAllowedError,
)
from framework_common.errors.standalones.validation import (
    ValueValidationRangeError as _ValueValidationRangeError,
)
from framework_common.errors.standalones.validation import (
    ValueValidationRequiredError as _ValueValidationRequiredError,
)


class ContainerErrorBase:
    """Expose reusable nested errors without making the container an exception."""

    # region Nested Classes

    class TypeValidationError(_TypeValidationError):
        """Share the property-based type error across all derived containers."""

    class ValueValidationError(_ValueValidationError):
        """Share the property-based value error across all derived containers."""

    class ValueValidationRequiredError(
        _ValueValidationRequiredError, ValueValidationError
    ):
        """Carry structured facts for ValueValidationRequiredError."""

    class ValueValidationLengthError(_ValueValidationLengthError, ValueValidationError):
        """Carry structured facts for ValueValidationLengthError."""

    class ValueValidationRangeError(_ValueValidationRangeError, ValueValidationError):
        """Carry structured facts for ValueValidationRangeError."""

    class ValueValidationFormatError(_ValueValidationFormatError, ValueValidationError):
        """Carry structured facts for ValueValidationFormatError."""

    class ValueValidationCharacterSetError(
        _ValueValidationCharacterSetError, ValueValidationError
    ):
        """Carry structured facts for ValueValidationCharacterSetError."""

    class ValueValidationNotAllowedError(
        _ValueValidationNotAllowedError, ValueValidationError
    ):
        """Carry structured facts for ValueValidationNotAllowedError."""

    class ValueValidationExactlyOneRequiredError(
        _ValueValidationExactlyOneRequiredError, ValueValidationError
    ):
        """Report a parameter group requiring exactly one supplied value."""

    class ValueValidationMustDifferError(
        _ValueValidationMustDifferError, ValueValidationError
    ):
        """Carry structured facts for ValueValidationMustDifferError."""

    # endregion Nested Classes
