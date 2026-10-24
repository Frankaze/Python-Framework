# Framework Repository

Reusable SQLAlchemy repository and transaction foundations for Python 3.13+.

- `entity_base.py`: shared entity mixin; each application owns its ORM registry.
- `repository_base.py`: generic entity access and dynamic queries using an
  externally owned Session; it does not commit, roll back, or close the Session.
- `unit_of_work.py`: lazy Session creation and explicit root/child transaction
  ownership. Children share the root Session and rollback-only state. Leaving
  the root context rolls back uncommitted changes and closes it, without an
  automatic commit. Children are not SQL SAVEPOINTs.

## Application entity base

Create one declarative base per application, combining the Framework mixin with
SQLAlchemy's `DeclarativeBase`. Concrete table entities inherit this application
base. Each application gets a separate registry and metadata.

```python
from sqlalchemy.orm import DeclarativeBase

from framework_repository import EntityBase as FrameworkEntityBase


class EntityBase(FrameworkEntityBase, DeclarativeBase):
    """Application-owned declarative base for mapped entities."""
```

Applications may similarly subclass `RepositoryBase` to provide their own shared
repository behavior. The inherited `create_sub_unit()` returns a Framework
`UnitOfWork`, matching the original implementation.

## Dependencies and migration status

The implementation requires SQLAlchemy; it does not use pyodbc directly. The
application selects and configures its database driver and Session factory.
SQLAlchemy is declared as `sqlalchemy>=2.1.4`. Run `uv sync` in this package
directory to create or synchronize its environment using `uv.lock`.
ILeague currently retains its original implementation and has not switched its
dependencies or imports to this package.
