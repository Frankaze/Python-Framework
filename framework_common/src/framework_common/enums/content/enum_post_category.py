"""Post categories for authored content."""

from enum import Enum


class EnumPostCategory(Enum):
    """Separate official announcements, development notes, and release notes."""

    # region Constants

    ANNOUNCEMENT: str = "Announcement"
    DEV_LOG: str = "DevLog"
    RELEASE: str = "Release"

    # endregion Constants
