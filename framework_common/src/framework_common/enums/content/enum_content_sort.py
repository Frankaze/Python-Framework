"""Named list orders shared by authored content."""

from enum import Enum


class EnumContentSort(Enum):
    """Name complete orders instead of exposing columns and directions.

    Each member ends with the primary key as a tie-breaker so pages stay stable.
    FEED needs a pinned flag and SEQUENCE a manual sequence number; services
    declare which members they support and reject the rest instead of falling
    back to another order.
    """

    # region Constants

    FEED: str = "Feed"
    LATEST_PUBLISHED: str = "LatestPublished"
    OLDEST_PUBLISHED: str = "OldestPublished"
    RECENTLY_UPDATED: str = "RecentlyUpdated"
    RECENTLY_CREATED: str = "RecentlyCreated"
    SEQUENCE: str = "Sequence"

    # endregion Constants
