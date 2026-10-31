"""Reject a crawl that cannot control commits inside a child unit of work."""

from framework_common.errors.error_base import ErrorBase


class CrawlSubUnitOfWorkNotAllowedError(ErrorBase):
    """Report a crawl invoked with a child unit of work, without response text."""
