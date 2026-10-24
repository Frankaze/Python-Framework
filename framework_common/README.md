# Framework Common

Shared foundations for Python applications. Requires Python 3.13 or later and
has no third-party runtime dependencies.

- `functions/function_enum.py`: resolve enum members by name, ignoring case.
  Unknown names return `None`; input is not trimmed and values are not matched.
- `enums/enum_month.py`: calendar months with numeric values from 1 to 12.
- `exceptions/exception_base.py`: base exception for application-specific errors.

```python
from framework_common.enums import EnumMonth
from framework_common.exceptions import ExceptionBase
from framework_common.functions import function_enum
```

Applications can subclass `ExceptionBase` for their own exception hierarchy.
Business-specific enums such as ILeague's `EnumChampionClass` remain in the
application. ILeague currently retains its original Common implementation and
has not yet switched its dependencies or imports to this package.
