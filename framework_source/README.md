# Framework Source

Shared configuration for external data sources. Requires Python 3.13 or later
and has no third-party runtime dependencies.

```python
from framework_source.source_base import SourceBase
```

`SourceBase` remains in `framework_source/source_base.py`, matching applications
that keep their shared source base at the package root, alongside source groups
such as `data/` and `intelligence/`. No empty source groups are created here.

`SourceBase` exposes read-only `timeout` and `request_interval` properties,
defaulting to 30.0 and 1.0 seconds respectively. It stores these settings without
opening connections, sending requests, or enforcing request timing. Concrete
source clients are responsible for applying them.

Applications can subclass `SourceBase` for application-wide behavior before
implementing their concrete sources. Website-specific clients, parsers, and
source models remain in the application.
