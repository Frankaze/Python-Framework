"""Publication states shared by authored content."""

from enum import Enum


class EnumContentPublishStatus(Enum):
    """Distinguish drafts, visible, manually withdrawn, and expired content.

    EXPIRED is set by a scheduled job when time-bound content, such as an
    announcement, passes its end time; content without an end time never uses it.
    """

    # region Constants

    DRAFT: str = "Draft"
    PUBLISHED: str = "Published"
    ARCHIVED: str = "Archived"
    EXPIRED: str = "Expired"

    # endregion Constants
