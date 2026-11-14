# Python Framework

Reusable Python application foundations. Maintained by Frankaze. Requires
Python 3.13 or later.

| Package | Shared functionality |
| --- | --- |
| [framework_common](framework_common/README.md) | Enum helpers, calendar months, timeframe units, supported languages, API error codes with English/Traditional Chinese/Korean messages, and base errors |
| [framework_repository](framework_repository/README.md) | Entity mixin, common/definition/transaction Repository bases, and root/child UnitOfWork |
| [framework_service](framework_service/README.md) | Service lifecycle, DmAssignedBase, query validation, and partial-update mapping |
| [framework_source](framework_source/README.md) | Shared source timeout and request interval settings |
| [framework_fastapi](framework_fastapi/README.md) | ControllerBase, application-configured ModelBase, and endpoint-retirement dependency; depends on Common |

## Development

Each package has its own `pyproject.toml`, `uv.lock`, and local environment when
synchronized. This repository is not a uv workspace. Run uv commands from the
package directory you want to develop:

```powershell
cd framework_service
uv sync
```

Service references Repository through an editable sibling path. Preserve the
relative package layout on Windows and macOS, and run `uv sync` on each machine.
Virtual environments and caches are excluded from Git; commit source files,
project configuration, `.python-version`, and lockfiles.

## Application boundaries

Framework packages do not depend on consuming applications. Business entities,
models, parsers, enums, settings, environment files, and database drivers belong
to applications.
Applications keep their own Base classes for project-specific behavior.

Base class modules use the same role folders as consuming applications:

| Package | Class locations |
| --- | --- |
| Repository | `models/entity_base.py`; `repositories/repository_base.py`, `repository_definition_base.py`, and `repository_transaction_base.py` |
| Service | `models/dm_assigned_base.py`; `services/service_base.py` and `service_crawl_base.py` |
| Source | `source_base.py` at the package root, shared by source groups |
| FastAPI | `controllers/controller_base.py`; `controllers/dependencies/`; `models/model_base.py` |

`UnitOfWork` remains in `framework_repository/unit_of_work.py`. Applications
import classes directly from their defining modules, matching their directory layout.

Each application combines the Framework entity mixin with SQLAlchemy
`DeclarativeBase` to own its registry and metadata. API models receive an
application-owned Engine factory; application shutdown must call `close()`
after ongoing operations finish. The FastAPI package directly depends on FastAPI
and Common and exposes reusable request dependencies. Shared enums remain in
Common; HTTP-specific checks and response construction belong to FastAPI.

This repository currently supports local development through uv path
dependencies; remote publishing and deployment are not configured.

## Direct module imports

All package-root `__init__.py` files are empty. Import classes from their defining modules, for example `from framework_service.services.service_base import ServiceBase` and `from framework_repository.unit_of_work import UnitOfWork`. Subpackage initializers do not re-export classes. Moving a class requires updating consumers to its actual module path.
