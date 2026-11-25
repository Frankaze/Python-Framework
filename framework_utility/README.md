# Framework Utility

Shared runtime utilities for Python applications. Requires Python 3.13 or
later. The initial package provides the dependency setup for future utilities.

`framework-utility` depends on `framework-common` through an editable sibling
path. Run `uv sync --locked` from this package directory to set up its local
environment.

To reference the package from an application under `src/<package>/` in a
repository next to Python Framework, run this from that application package:

```powershell
uv add --editable ../../../python-framework/framework_utility
```

From a sibling package within Python Framework, use
`uv add --editable ../framework_utility`. Add a direct dependency wherever the
package is imported.
