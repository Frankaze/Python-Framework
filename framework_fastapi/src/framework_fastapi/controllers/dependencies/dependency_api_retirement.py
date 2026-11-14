"""Reusable dependencies for API endpoint lifecycle checks."""

from collections.abc import Callable
from typing import NoReturn

from fastapi import HTTPException, status

from framework_common.enums.enum_api_error_code import EnumApiErrorCode
from framework_common.enums.enum_language import EnumLanguage


def create_api_retirement_dependency(
    str_replacement: str | None = None,
    enm_language: EnumLanguage = EnumLanguage.EN_US,
) -> Callable[[], NoReturn]:
    """Create a dependency that rejects a retired endpoint with HTTP 410.

    The replacement is advisory metadata, not a redirect. Creating the
    dependency does not raise; FastAPI invokes it when handling a request.
    The language is fixed when creating the dependency, defaulting to English.
    """

    def _reject_request() -> NoReturn:
        """Stop the request before its endpoint handler executes."""
        _enm_error: EnumApiErrorCode = EnumApiErrorCode.API_RETIRED
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail={
                "code": _enm_error.value,
                "message": _enm_error.get_message(enm_language),
                "replacement": str_replacement,
            },
        )

    return _reject_request
