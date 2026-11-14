"""Shared API error codes and standard localized messages."""

from enum import Enum

from framework_common.enums.enum_language import EnumLanguage


class EnumApiErrorCode(Enum):
    """Define public API error identifiers independently of HTTP status codes."""

    # region Constants

    API_RETIRED: str = "API_RETIRED"
    TOKEN_INVALID: str = "TOKEN_INVALID"

    # endregion Constants

    # region Properties

    @property
    def message_en(self) -> str:
        """Return the standard English message for this error code."""
        _dic_messages: dict[EnumApiErrorCode, str] = {
            EnumApiErrorCode.API_RETIRED: "This API endpoint has been retired.",
            EnumApiErrorCode.TOKEN_INVALID: "Invalid authentication token.",
        }
        return _dic_messages[self]

    @property
    def message_zh_tw(self) -> str:
        """Return the standard Traditional Chinese message for this error code."""
        _dic_messages: dict[EnumApiErrorCode, str] = {
            EnumApiErrorCode.API_RETIRED: "此 API 端點已停止服務。",
            EnumApiErrorCode.TOKEN_INVALID: "驗證權杖無效。",
        }
        return _dic_messages[self]

    @property
    def message_ko_kr(self) -> str:
        """Return the standard Korean message for this error code."""
        _dic_messages: dict[EnumApiErrorCode, str] = {
            EnumApiErrorCode.API_RETIRED: "이 API 엔드포인트는 더 이상 제공되지 않습니다.",
            EnumApiErrorCode.TOKEN_INVALID: "유효하지 않은 인증 토큰입니다.",
        }
        return _dic_messages[self]

    # endregion Properties

    # region Public Methods

    def get_message(self, enm_language: EnumLanguage = EnumLanguage.EN_US) -> str:
        """Return the standard message in the explicitly selected language."""
        _dic_messages: dict[EnumLanguage, str] = {
            EnumLanguage.EN_US: self.message_en,
            EnumLanguage.ZH_TW: self.message_zh_tw,
            EnumLanguage.KO_KR: self.message_ko_kr,
        }
        return _dic_messages[enm_language]

    # endregion Public Methods
