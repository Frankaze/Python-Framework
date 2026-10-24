# Python Framework

Reusable Python application foundations. Maintained by Frankaze. Requires
Python 3.13 or later.

| Package | Shared functionality |
| --- | --- |
| [framework_common](framework_common/README.md) | Enum helpers, calendar months, and base exceptions |
| [framework_repository](framework_repository/README.md) | Entity mixin, common/definition/transaction Repository bases, and root/child UnitOfWork |
| [framework_service](framework_service/README.md) | Service lifecycle, DmAssignedBase, query validation, and partial-update mapping |
| [framework_source](framework_source/README.md) | Shared source timeout and request interval settings |
| [framework_fastapi](framework_fastapi/README.md) | ControllerBase and application-configured ModelBase |

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

Each application combines the Framework entity mixin with SQLAlchemy
`DeclarativeBase` to own its registry and metadata. API models receive an
application-owned Engine factory; application shutdown must call `close()`
after ongoing operations finish. The current FastAPI package does not yet
include FastAPI-specific routing behavior or require FastAPI itself.

This repository currently supports local development through uv path
dependencies; remote publishing and deployment are not configured.
