"""Structured errors for crawl."""

from framework_common.errors.standalones.crawl.crawl_already_running_error import (
    CrawlAlreadyRunningError,
)
from framework_common.errors.standalones.crawl.crawl_scope_required_error import (
    CrawlScopeRequiredError,
)
from framework_common.errors.standalones.crawl.crawl_sub_unit_of_work_not_allowed_error import (
    CrawlSubUnitOfWorkNotAllowedError,
)

__all__: list[str] = [
    "CrawlAlreadyRunningError",
    "CrawlScopeRequiredError",
    "CrawlSubUnitOfWorkNotAllowedError",
]
