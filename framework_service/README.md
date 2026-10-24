# Framework Service

Shared service lifecycle and query mapping for Python 3.13+.

```python
from framework_service import ServiceBase
```

`ServiceBase` accepts exactly one of a Session factory or an existing Framework
`UnitOfWork`. It creates a root UoW for a factory, or uses the supplied UoW as-is,
and delegates context entry and exit to it. Commits remain explicit. Compose
services by supplying child UoWs when their operations must share a transaction.

`ServiceBase.MapperBase[TQuery]` defines the abstract static `to_conditions()`
contract. The internal `_get_query_conditions()` helper rejects `None` and
queries mapping to no conditions, without creating a Session or running SQL.
Concrete mappers and business Domain Models remain in the application.

The implementation declares `sqlalchemy>=2.1.4` directly and imports `UnitOfWork`
from `framework_repository`, referenced through the editable relative path
`../framework_repository`. Keep both packages as sibling directories and run
`uv sync` in this package directory to create or synchronize its environment
using `uv.lock`.

ILeague retains its original ServiceBase and has not switched its dependencies
or imports to this package.
