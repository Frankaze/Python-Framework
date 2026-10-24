# Framework Repository

Reusable SQLAlchemy repository and transaction foundations for Python 3.13+.

This package owns the shared SQLAlchemy version pin: `sqlalchemy==2.1.8` in
pyproject.toml. Consumers that import SQLAlchemy keep an unversioned direct
dependency and inherit this version through their Repository dependency chain.
After changing the pin, refresh each affected package's lockfile and environment.

- `models/entity_base.py`: shared entity mixin; each application owns its ORM registry.
- `repositories/repository_base.py`: generic entity access and dynamic queries using an
  externally owned Session; it does not commit, roll back, or close the Session.
- `repositories/repository_definition_base.py`: `RepositoryDefinitionBase`, extending common
  operations for configuration/master data with application-owned business keys.
- `repositories/repository_transaction_base.py`: `RepositoryTransactionBase`, adding
  `get_by_id(int_id, *, lst_ormo_options=None)` for integer transaction keys.
- `unit_of_work.py`: lazy Session creation and explicit root/child transaction
  ownership. Children share the root Session and rollback-only state. Leaving
  the root context rolls back uncommitted changes and closes it, without an
  automatic commit. Children are not SQL SAVEPOINTs.

## Structure and imports

```text
framework_repository/
├── __init__.py
├── unit_of_work.py
├── models/
│   ├── __init__.py
│   └── entity_base.py
└── repositories/
    ├── __init__.py
    ├── repository_base.py
    ├── repository_definition_base.py
    └── repository_transaction_base.py
```

```python
from framework_repository.unit_of_work import UnitOfWork
from framework_repository.models.entity_base import EntityBase
from framework_repository.repositories.repository_base import RepositoryBase
from framework_repository.repositories.repository_definition_base import (
    RepositoryDefinitionBase,
)
from framework_repository.repositories.repository_transaction_base import (
    RepositoryTransactionBase,
)
```

Class modules follow the same role folders as consuming applications. UnitOfWork
remains package-level transaction infrastructure. Import each class from its
defining module; package initializers do not re-export classes.

## Persistence errors

UoW lifecycle checks use `PersistenceError` from
`framework_common.errors.containers.persistence_error`. Re-entering an active context raises
`AlreadyActiveError`; accessing a closed context raises `ClosedError`, whose
`method` identifies the requested operation. A rollback-only transaction rejects
commit/flush with `TransactionMarkedForRollbackError`, also carrying `method`.
A child `rollback()` first marks the shared transaction rollback-only, then
raises `TransactionRollbackRequestedError`. Propagation out of the root context
causes the actual rollback; catching the request does not clear the shared flag.
Root rollback executes immediately and clears it. These errors contain no
response messages and do not inherit function-validation errors. Original
database exceptions continue to propagate unchanged.

## Application entity base

Create one declarative base per application, combining the Framework mixin with
SQLAlchemy's `DeclarativeBase`. Concrete table entities inherit this application
base. Each application gets a separate registry and metadata.

```python
from sqlalchemy.orm import DeclarativeBase

from framework_repository.models.entity_base import EntityBase as FrameworkEntityBase


class EntityBase(FrameworkEntityBase, DeclarativeBase):
    """Application-owned declarative base for mapped entities."""
```

## Repository hierarchy

```text
RepositoryBase[TEntity]
├── RepositoryDefinitionBase[TEntity]
└── RepositoryTransactionBase[TEntity]
```

The common base provides `get_many`, `get_first`, `add`, and `delete`. Only the
transaction subclass provides `get_by_id`; missing IDs return `None`. Loader
options refresh cached entities through `populate_existing` as before.

Definition repositories implement business-key methods such as `get_by_name`
or `get_by_version` using the common query operations. Each application may
subclass the appropriate Framework base for its own shared behavior. Existing
consumers of `RepositoryBase.get_by_id` must switch to
`RepositoryTransactionBase`; there is no compatibility alias on the common base.
`EntityBase` remains shared and does not define an ID column.

## Operation-aware updates

`apply_update(ent_entity, dic_values, dic_enm_operations=None)` stages changes to
a tracked ORM entity and returns whether a write was staged. Operand dictionary
keys and operation dictionary keys are ORM attribute names. Omitted operations
default to `EnumUpdateOperation.ASSIGN`; no Domain Model or raw tuple is accepted.

- Assign replaces a value and skips equal values.
- Increment stages `column = column + operand` for numeric columns.
- Append stages SQL string concatenation for text columns.

All operation operands are checked before mutating the entity. Existing pending
assignments or SQL expressions are preserved when composing another operation.
SQL expressions reference database values rather than stale Python calculations.
Before flush, an operated ORM attribute may hold a SQL expression; SQLAlchemy
expires that attribute after flush and reads its result on subsequent access.

NULL propagates; the method does not treat it as zero or empty text. Increment
by zero and Append of empty text skip writes. Other relative operations count as
staged writes, including operations on NULL. Application mappers validate schema
capacity; the database enforces constraints on the resulting stored values.
Audit fields remain service-owned. No explicit flush or commit is performed.

Repositories share the UoW-owned Session and never submit transactions themselves.
`UnitOfWork.create_sub_unit()` returns a Framework `UnitOfWork` with the same
transaction ownership rules.

## Dependencies

The implementation requires SQLAlchemy; it does not use pyodbc directly. The
application selects and configures its database driver and Session factory.
SQLAlchemy is pinned to `sqlalchemy==2.1.8`. Run `uv sync` in this package
directory to create or synchronize its environment using `uv.lock`.
