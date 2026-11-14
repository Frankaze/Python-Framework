"""Shared language tags supported by localized application messages."""

from enum import Enum


class EnumLanguage(Enum):
    """Define supported languages using language and region tags."""

    # region Constants

    EN_US: str = "en-US"
    ZH_TW: str = "zh-TW"
    KO_KR: str = "ko-KR"

    # endregion Constants
