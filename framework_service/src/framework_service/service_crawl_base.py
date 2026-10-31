"""Service foundation for nonblocking crawl ownership on a single host."""

import errno
import os
from collections.abc import Callable, Generator
from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
from tempfile import gettempdir
from typing import BinaryIO

from framework_common.errors.standalones.crawl import (
    CrawlAlreadyRunningError,
    CrawlScopeRequiredError,
)
from framework_service.service_base import ServiceBase


class ServiceCrawlBase(ServiceBase):
    """Add crawl exclusion while leaving persistence and commit policy to services."""

    # region Internal Methods

    @staticmethod
    @contextmanager
    def _crawl_scope(
        str_scope: str,
        *,
        fnc_running_error: Callable[[], CrawlAlreadyRunningError] | None = None,
    ) -> Generator[None, None, None]:
        """Hold an OS file lock until scope exit, including exceptional exits.

        Processes must share a host and temp directory. Keep the lock file so
        contenders always lock the same file. Process exit releases ownership.
        """
        if not str_scope.strip():
            raise CrawlScopeRequiredError()
        _str_digest: str = sha256(str_scope.encode("utf-8")).hexdigest()
        _path_lock: Path = Path(gettempdir()) / f"framework-crawl-{_str_digest}.lock"
        _file_lock: BinaryIO = _path_lock.open("a+b")
        try:
            try:
                if os.name == "nt":
                    import msvcrt

                    if _file_lock.seek(0, os.SEEK_END) == 0:
                        _file_lock.write(b"\0")
                        _file_lock.flush()
                    _file_lock.seek(0)
                    msvcrt.locking(_file_lock.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl

                    fcntl.flock(_file_lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as _exc_lock:
                if _exc_lock.errno in (errno.EACCES, errno.EAGAIN, errno.EDEADLK):
                    if fnc_running_error is not None:
                        raise fnc_running_error() from _exc_lock
                    raise CrawlAlreadyRunningError(str_target=str_scope) from _exc_lock
                raise
            yield
        finally:
            _file_lock.close()

    # endregion Internal Methods
