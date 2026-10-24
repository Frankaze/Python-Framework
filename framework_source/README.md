# Framework Source

Shared configuration for external data sources. Requires Python 3.13 or later
and has no third-party runtime dependencies.

```python
from framework_source import SourceBase
```

`SourceBase` exposes read-only `timeout` and `request_interval` properties,
defaulting to 30.0 and 1.0 seconds respectively. It stores these settings without
opening connections, sending requests, or enforcing request timing. Concrete
source clients are responsible for applying them.

Applications can subclass `SourceBase` for application-wide behavior before
implementing their concrete sources. Website-specific clients, parsers, and
source models remain in the application.

ILeague currently retains its original SourceBase and has not switched its
dependencies or imports to this package.
