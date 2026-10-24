# Framework FastAPI

Reusable controller and API model foundations for Python 3.13+.

```python
from framework_fastapi import ControllerBase, ModelBase
```

- `controller_base.py`: extension point for lightweight HTTP controllers.
- `model_base.py`: lazy, locked initialization and caching of an application-
  supplied SQLAlchemy Engine and its Session factory.

## Application configuration

Pass a no-argument Engine factory to `ModelBase`. It is called on the first
`_create_session_factory()` access, not during model construction. It must
return a new Engine owned by that model; returning a shared Engine would allow
one model's `close()` to dispose another model's pool.

The application's ModelBase can preserve its Settings-based constructor, build
the database URL in an internal factory method, and pass that bound method to
the Framework constructor. Settings loading, environment paths, credentials,
database dialects, and driver configuration remain in the application.

Each model instance caches its own Engine and sessionmaker. Pass the factory
to a new Service/UoW per operation. Do not share a Session across concurrent
requests. Initialization failures leave the model available for retry.

Call `close()` from application lifespan shutdown after operations have
finished. It disposes the cached Engine and clears the cache. Repeated close
calls are safe; later factory access can initialize a new Engine. Cleanup is
not wired automatically, and `close()` does not close outstanding Sessions.

## Dependencies and migration status

The current bases directly use SQLAlchemy, but do not import FastAPI, pyodbc,
or pydantic-settings. Add framework-specific dependencies only when needed by
actual shared functionality. SQLAlchemy is declared as `sqlalchemy>=2.1.4`.
Run `uv sync` in this package directory to create or synchronize its environment
using `uv.lock`.

ILeague retains its existing ControllerBase, ModelBase, and Settings. Its
dependencies, inheritance, and application lifespan have not yet been changed.
