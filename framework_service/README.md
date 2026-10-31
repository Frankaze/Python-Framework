# Framework Service

Shared service lifecycle, assignment tracking, query mapping, and partial updates
for Python 3.13+.

```python
from framework_service import DmAssignedBase, ServiceBase, ServiceCrawlBase
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
arguments raise `ValueValidationNotAllowedError` before setters are called.

## Query and update mapping

`ServiceBase.MapperBase[TQuery]` defines the abstract class method `to_conditions()`
contract, with `TQuery` bounded by `DmAssignedBase`. `_get_query_conditions()`
rejects a missing or unassigned query and empty mapped conditions, without
creating a Session or running SQL. Application mappers map assigned `None` to
`IS NULL`; omitted fields generate no predicate.

`ServiceBase.UpdateMapperBase[TUpdate]` defines the abstract class method
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

Mapper base methods retain `@abstractmethod` and use `@classmethod` so their
fallback can identify the calling subclass. An inherited or explicitly invoked
base implementation raises `FunctionValidationNotImplementedError`, carrying
`owner_type=cls` and the base function object in `method`. Existing concrete
static-method overrides remain supported. Python's ABC instantiation checks
remain in effect; these errors do not replace interpreter-generated TypeError.

`DmAssignedBase._assign_fields()` rejects unknown constructor argument names with
`ValueValidationNotAllowedError` before invoking any setters. The field is the
`dic_values` Parameter, the actual value is the alphabetically first unknown
name, and allowed values contain the sorted supported argument names. This
validates names without retaining supplied values or formatting a message.

## Crawl Ownership

`ServiceCrawlBase` extends `ServiceBase` for services that perform crawls.
`ServiceCrawlBase._crawl_scope(scope)` is a context manager owning a nonblocking
OS file lock. Lock acquisition and release are implemented within this base;
there is no separate public `CrawlGuard`. General services inherit `ServiceBase`,
which has no crawl-specific methods. Use the
same application scope across services that must not crawl concurrently. Hold
it through source access, persistence, commit and failure rollback. Contention
raises `framework_common.errors.standalones.crawl.CrawlAlreadyRunningError`; the HTTP layer decides
the response status. This adds no implicit transaction or commit behavior.

Windows uses `msvcrt.locking`, Unix uses `fcntl.flock`. Workers must share the
host temp directory and scope. Locks release on close or process termination;
persistent lock files must not be removed while workers may use them. Separate
hosts or isolated container temp directories require distributed coordination.


Pass `fnc_running_error` to `_crawl_scope` to select an application error factory,
for example `PatchError.CrawlAlreadyRunningError`. The scope instantiates it only on
contention. This preserves Framework independence from application classes.
