# Framework Service

Shared service lifecycle, assignment tracking, query mapping, and partial updates
for Python 3.13+.

```python
from framework_service import DmAssignedBase, ServiceBase
```

`ServiceBase` accepts exactly one of a Session factory or an existing Framework
`UnitOfWork`. It creates a root UoW for a factory, or uses the supplied UoW as-is,
and delegates context entry and exit to it. Commits remain explicit. Compose
services by supplying child UoWs when their operations must share a transaction.

## Assigned Query and Update models

`DmAssignedBase` tracks explicit assignments in an internal set and exposes an
immutable `assigned_fields` snapshot. Model constructors initialize backing fields
directly; property setters assign values and register their property names.
Default `None` values are unassigned. Explicitly setting a field to `None` marks
it assigned, just as assigning `False`, zero, or any other value does.

Applications subclass this base and define their own Query and Update fields.
Read and Create models need not inherit it. Updates are independent models;
they do not inherit Create fields or assume the same allowed attributes.
The protected `_assign_fields()` helper routes supplied constructor keywords
through setters using an application-defined argument-to-property map. Omitted
keywords stay unassigned; explicitly supplied `None` is assigned. Unknown
arguments raise `TypeError` before setters are called.

## Query and update mapping

`ServiceBase.MapperBase[TQuery]` defines the abstract static `to_conditions()`
contract, with `TQuery` bounded by `DmAssignedBase`. `_get_query_conditions()`
rejects a missing or unassigned query and empty mapped conditions, without
creating a Session or running SQL. Application mappers map assigned `None` to
`IS NULL`; omitted fields generate no predicate.

`ServiceBase.UpdateMapperBase[TUpdate]` defines the abstract static
`to_update_values()` contract. Application mappers validate every assigned value
and return a dictionary of ORM attribute names and converted values. Explicit
`None` means SQL NULL and must be rejected for non-nullable fields as appropriate.
This supports property/column renaming and application-specific Enum conversion.

`_get_update_values()` rejects a missing/unassigned update and empty mappings.
`_apply_update(entity, update, mapper)` validates all mapped values, determines
which attributes differ, applies only those changes, and returns a bool. It does
not query, attach detached objects, mutate audit timestamps, or flush/commit.
Applications use tracked Session entities, enforce business rules, update their
own audit fields only when changed, and retain their transaction boundaries.

The implementation declares `sqlalchemy>=2.1.4` directly and imports `UnitOfWork`
from `framework_repository`, referenced through the editable relative path
`../framework_repository`. Keep both packages as sibling directories and run
`uv sync` in this package directory to create or synchronize its environment
using `uv.lock`.
