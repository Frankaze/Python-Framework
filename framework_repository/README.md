# Framework Repository

Reusable SQLAlchemy repository and transaction foundations for Python 3.13+.

- `entity_base.py`: shared entity mixin; each application owns its ORM registry.
- `repository_base.py`: generic entity access and dynamic queries using an
  externally owned Session; it does not commit, roll back, or close the Session.
- `repository_definition_base.py`: `RepositoryDefinitionBase`, extending common
  operations for configuration/master data with application-owned business keys.
- `repository_transaction_base.py`: `RepositoryTransactionBase`, adding
  `get_by_id(int_id, *, lst_ormo_options=None)` for integer transaction keys.
- `unit_of_work.py`: lazy Session creation and explicit root/child transaction
  ownership. Children share the root Session and rollback-only state. Leaving
  the root context rolls back uncommitted changes and closes it, without an
  automatic commit. Children are not SQL SAVEPOINTs.

## Persistence errors

UoW lifecycle checks use `PersistenceError` from
`framework_common.errors.containers`. Re-entering an active context raises
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

from framework_repository import EntityBase as FrameworkEntityBase


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

Repositories share the UoW-owned Session and never submit transactions themselves.
`UnitOfWork.create_sub_unit()` returns a Framework `UnitOfWork` with the same
transaction ownership rules.

## Dependencies

The implementation requires SQLAlchemy; it does not use pyodbc directly. The
application selects and configures its database driver and Session factory.
SQLAlchemy is declared as `sqlalchemy>=2.1.4`. Run `uv sync` in this package
directory to create or synchronize its environment using `uv.lock`.
