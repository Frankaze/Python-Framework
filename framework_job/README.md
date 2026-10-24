# Framework Job

Reusable job package maintained by Frankaze. Requires Python 3.13 or later.

This initial scaffold owns the shared `APScheduler ==3.11.3` version pin.
The resolved version is recorded in `uv.lock`. The package root `__init__.py`
is empty and `py.typed` is included, matching the other Framework packages.

## Development

Run commands from this package directory:

```powershell
uv sync --locked
```

This package has its own virtual environment and lockfile. It is not part of a
uv workspace and does not depend on any consuming application's packages.

Consumers depend on framework_job through an editable relative path and inherit
the APScheduler version. Change this package's pin to upgrade APScheduler, then
refresh the affected consumers' lockfiles and environments. Consumers that
import APScheduler directly declare it without their own version specifier.

## Current scope

Job classes, scheduler configuration, registration, lifecycle management,
execution records, and error handling are pending design. Importing this
package does not start a scheduler or execute jobs. No sample jobs, Base
classes, or executable entry point have been added.

Official APScheduler documentation: <https://apscheduler.readthedocs.io/en/3.x/>.
