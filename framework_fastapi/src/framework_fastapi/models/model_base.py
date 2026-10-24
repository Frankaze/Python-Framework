"""Application-configured Engine and Session factory lifecycle for API models."""

from collections.abc import Callable
from threading import Lock

from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker


class ModelBase:
    """Lazily own an Engine supplied by an application-specific factory.

    The factory must return a new Engine owned by this model. Settings, database
    URLs, and driver choices belong to the application. Session factories may
    be shared; individual Sessions must not be shared across concurrent work.
    """

    # region Constructor & Special Methods

    def __init__(self, fnc_engine_factory: Callable[[], Engine]) -> None:
        self._fnc_engine_factory: Callable[[], Engine] = fnc_engine_factory
        self._engine: Engine | None = None
        self._fnc_session_factory: sessionmaker[Session] | None = None
        self._lock: Lock = Lock()

    # endregion Constructor & Special Methods

    # region Public Methods

    def close(self) -> None:
        """Dispose the cached Engine after all operations have finished.

        Call from application shutdown, not after each request. Later factory
        access can initialize a new Engine, matching the original lifecycle.
        """
        with self._lock:
            if self._engine is not None:
                self._engine.dispose()
            self._engine = None
            self._fnc_session_factory = None

    # endregion Public Methods

    # region Internal Methods

    def _create_session_factory(self) -> sessionmaker[Session]:
        """Create and cache a factory under a lock without opening a Session."""
        with self._lock:
            if self._fnc_session_factory is not None:
                return self._fnc_session_factory

            self._engine = self._fnc_engine_factory()
            self._fnc_session_factory = sessionmaker(bind=self._engine)
            return self._fnc_session_factory

    # endregion Internal Methods
