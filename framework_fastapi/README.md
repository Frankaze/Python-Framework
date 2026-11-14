# Framework FastAPI

Reusable controller and API model foundations for Python 3.13+.

```python
from framework_fastapi.controllers.controller_base import ControllerBase
from framework_fastapi.models.model_base import ModelBase
```

- `controllers/controller_base.py`: extension point for lightweight HTTP controllers.
- `models/model_base.py`: lazy, locked initialization and caching of an application-
  supplied SQLAlchemy Engine and its Session factory.

```text
framework_fastapi/
├── __init__.py
├── controllers/
│   ├── __init__.py
│   ├── controller_base.py
│   └── dependencies/
│       ├── __init__.py
│       └── dependency_api_retirement.py
└── models/
    ├── __init__.py
    └── model_base.py
```

Import classes and dependency factories directly from their defining modules;
package initializers do not re-export them.

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

## Endpoint retirement dependency

`controllers/dependencies/` contains reusable request dependencies. Each module
groups dependencies by purpose. `dependency_api_retirement.py` exposes
`create_api_retirement_dependency`, which creates a callable for FastAPI to invoke.

```python
from fastapi import APIRouter, Depends

from framework_common.enums.enum_language import EnumLanguage
from framework_fastapi.controllers.dependencies.dependency_api_retirement import create_api_retirement_dependency

_router: APIRouter = APIRouter(prefix="/api/v1/champion", tags=["Champion"])


def crawl() -> int:
    """Represent the endpoint handler that the dependency prevents from running."""
    return 0


_router.add_api_route(
    "/crawl",
    crawl,
    methods=["POST"],
    deprecated=True,
    dependencies=[
        Depends(
            create_api_retirement_dependency(
                str_replacement="/api/v3/champion/crawl",
                enm_language=EnumLanguage.KO_KR,
            )
        )
    ],
    responses={410: {"description": "This API endpoint has been retired."}},
)
```

The dependency raises HTTP 410 using Common's `EnumApiErrorCode.API_RETIRED`.
The default FastAPI response is `detail` containing `code`, a localized
`message`, and `replacement`. `enm_language` accepts Common's `EnumLanguage`:
`EN_US` (default), `ZH_TW`, or `KO_KR`. The example returns the Korean message
`이 API 엔드포인트는 더 이상 제공되지 않습니다.`. Language is fixed when creating
the dependency; it is not a request parameter and does not read request headers.
Omitted replacements serialize as null; no redirect occurs.
`deprecated=True` and the 410 response
description are separate OpenAPI declarations; the dependency does not set them.
Only the endpoint where the dependency is attached is rejected. No ILeague route
is retired automatically, and no token-validation dependency is implemented.

The package declares FastAPI directly. Request behavior is verified with an
isolated ASGI application; no consuming application's endpoints are modified.

## Package dependencies

This package directly depends on `framework_common` through the editable sibling
path `../framework_common`. Shared enums, including `EnumLanguage` and
`EnumApiErrorCode` with English, Traditional Chinese, and Korean messages, live in Common and are imported from
their defining modules under `framework_common.enums`; no FastAPI-specific Enum
copy or alias is retained.

The endpoint dependency uses FastAPI's `HTTPException` and HTTP status constants.
FastAPI is declared as `fastapi>=0.148.0` without CLI extras; the package does not
require pyodbc or pydantic-settings. SQLAlchemy is declared as `sqlalchemy>=2.1.4`.
Run `uv sync` in this package directory to create or synchronize its environment
using `uv.lock`.
