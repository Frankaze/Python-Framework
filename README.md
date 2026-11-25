# Python Framework

Reusable Python application foundations. Maintained by Frankaze. Requires
Python 3.13 or later.

| Package | Shared functionality |
| --- | --- |
| [framework_common](framework_common/README.md) | Enum helpers, calendar months, timeframe units, supported languages, API error codes with English/Traditional Chinese/Korean messages, and base errors |
| [framework_repository](framework_repository/README.md) | Entity mixin, common/definition/transaction Repository bases, and root/child UnitOfWork |
| [framework_service](framework_service/README.md) | Service lifecycle, DmAssignedBase, DmUpdateBase, query validation, and operation-aware partial updates |
| [framework_source](framework_source/README.md) | Shared source timeout and request interval settings |
| [framework_fastapi](framework_fastapi/README.md) | ControllerBase, application-configured ModelBase, and endpoint-retirement dependency; depends on Common and Repository |
| [framework_job](framework_job/README.md) | Installable job package scaffold with APScheduler 3.x; job abstractions and scheduling lifecycle are pending design |
| [framework_utility](framework_utility/README.md) | Installable runtime utility package with an editable dependency on Common |
| [framework_tool](framework_tool/README.md) | Development tools only (not a library): pinned Ruff version, shared `ruff.toml`, and check scripts for the Framework and its products |

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

Check code with the Ruff version pinned in `framework_tool`; the root
`ruff.toml` extends its shared rules and lists the Framework packages as
first-party:

```powershell
.\framework_tool\scripts\scpt_check_python.ps1
```

## Application boundaries

Framework packages do not depend on consuming applications. Business entities,
models, parsers, enums, settings, environment files, and database drivers belong
to applications.
Applications keep their own Base classes for project-specific behavior.

Base class modules use the same role folders as consuming applications:

| Package | Class locations |
| --- | --- |
| Repository | `models/entity_base.py`; `repositories/repository_base.py`, `repository_definition_base.py`, and `repository_transaction_base.py` |
| Service | `models/dm_assigned_base.py`; `services/application/service_base.py` and `service_crawl_base.py` |
| Source | `source_base.py` at the package root, shared by source groups |
| FastAPI | `controllers/controller_base.py`; `controllers/dependencies/`; `models/model_base.py` |

`UnitOfWork` remains in `framework_repository/unit_of_work.py`. Applications
import classes directly from their defining modules, matching their directory layout.

Each application combines the Framework entity mixin with SQLAlchemy
`DeclarativeBase` to own its registry and metadata. API models receive an
application-owned Engine factory; application shutdown must call `close()`
after ongoing operations finish. The FastAPI package directly depends on FastAPI
and Common, follows Repository's SQLAlchemy pin, and exposes reusable request dependencies. Shared enums remain in
Common; HTTP-specific checks and response construction belong to FastAPI.

This repository currently supports local development through uv path
dependencies; remote publishing and deployment are not configured.

## Shared dependency versions

Framework packages own the third-party version pins used by consumers:

| Dependency | Version authority | Current pin |
| --- | --- | --- |
| SQLAlchemy | framework_repository/pyproject.toml | `sqlalchemy==2.1.8` |
| FastAPI | framework_fastapi/pyproject.toml | `fastapi==0.162.2` |
| Pydantic | framework_fastapi/pyproject.toml | `pydantic==2.14.3` |
| APScheduler | framework_job/pyproject.toml | `apscheduler==3.11.3` |

`framework_repository/pyproject.toml` is the version authority for SQLAlchemy,
currently pinned to `sqlalchemy==2.1.8`. Other packages that import SQLAlchemy
declare `sqlalchemy` without a separate version bound and depend on
`framework_repository` directly or transitively. FastAPI also references the
Repository package so its standalone environment follows the same version.

Each virtual environment installs its own copy of the resolved dependency;
it does not use another package's `.venv`. To change the shared SQLAlchemy
version, update the Repository pin, then run `uv lock` and `uv sync --locked`
in each affected package. Independent lockfiles do not update automatically
when the Framework declaration changes.

Imports still use SQLAlchemy's public modules directly. Framework packages
do not re-export third-party classes or turn API models into Repository users.

FastAPI and Pydantic follow the same rule: consuming APIs retain unversioned
direct dependencies and choose their FastAPI extras. Applications using Job
inherit APScheduler from framework_job; APIs do not acquire APScheduler unless
they depend on a package that requires it. Common and Source do not acquire web
or scheduling dependencies through this policy.

Both IndicatorBlitz and ILeague use editable Framework sources during local
development. Updating the Framework pins and refreshing consumers applies the
same versions without editing version numbers in the products. Merely bumping
a Framework package's version does not select new third-party versions, rewrite
other lockfiles, or reload already-running applications.

After updating the relevant pins, the following PowerShell block, run from this
repository root, refreshes Framework and both products together. It preserves
existing locked versions unless the new constraints require changes:

```powershell
$lst_str_projects = @(
    "framework_repository",
    "framework_service",
    "framework_fastapi",
    "framework_job",
    "../indicator-blitz/src/indicatorblitz_repository",
    "../indicator-blitz/src/indicatorblitz_service",
    "../indicator-blitz/src/indicatorblitz_api",
    "../indicator-blitz/src/indicatorblitz_job",
    "../ileague/src/ileague_repository",
    "../ileague/src/ileague_service",
    "../ileague/src/ileague_api"
)
foreach ($str_project in $lst_str_projects) {
    uv lock --project $str_project
    if ($LASTEXITCODE -ne 0) { throw "Lock failed: $str_project" }
    uv sync --locked --project $str_project
    if ($LASTEXITCODE -ne 0) { throw "Sync failed: $str_project" }
}
```

Commit each repository's changed dependency declarations and lockfiles together
after review. CI uses `uv sync --locked`; it does not silently rewrite lockfiles.

## Direct module imports

All package-root `__init__.py` files are empty. Import classes from their defining modules, for example `from framework_service.services.application.service_base import ServiceBase` and `from framework_repository.unit_of_work import UnitOfWork`. Subpackage initializers do not re-export classes. Moving a class requires updating consumers to its actual module path.
