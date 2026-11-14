# Framework Common

Shared foundations for Python applications. Requires Python 3.13 or later and
has no third-party runtime dependencies.

- `functions/function_enum.py`: resolve enum members by name, ignoring case.
  Unknown names return `None`; input is not trimmed and values are not matched.
- `functions/function_string.py`: `validate()` checks text type, nullability,
  blank values, length, ASCII and surrounding whitespace according to supplied rules.
- `functions/function_integer.py`: `validate()` checks exact integer type
  (excluding bool), nullability and inclusive bounds.
- `enums/enum_month.py`: calendar months with numeric values from 1 to 12.
- `enums/enum_language.py`: `EnumLanguage` with `EN_US` (`en-US`),
  `ZH_TW` (`zh-TW`), and `KO_KR` (`ko-KR`).
- `enums/enum_timeframe.py`: `EnumTimeframe` with Second, Minute, Hour, Day,
  Week, Month, Quarter, and Year string values; no abbreviations or multipliers.
- `errors/error_base.py`: base exception for application-specific errors.
- `errors/container_error_base.py`: extension point for public error containers.
- `errors/containers/persistence_error.py`: `PersistenceError` groups nested
  `AlreadyActiveError`, `ClosedError`, `TransactionMarkedForRollbackError` and
  `TransactionRollbackRequestedError`. They directly inherit `ErrorBase`.
  Closed/marked errors carry the attempted `method` function as read-only
  metadata. The container itself is not an exception; import it directly from
  `framework_common.errors.containers.persistence_error`.
- `errors/standalones/crawl/crawl_already_running_error.py`: reject a crawl while another
  crawl holds the shared coordination scope.
- `errors/standalones/validation/type_validation_error.py`: describe a type mismatch with
  a property descriptor, expected type, actual type, and whether None is allowed.
- `errors/standalones/validation/value_validation_error.py`: carry a property descriptor or `inspect.Parameter`,
  expected value and rejected actual value without formatting a message. This
  module contains `ValueValidationError` and every `ValueValidation...Error` subtype:
  Required, Length, Range, Format, CharacterSet, NotAllowed, ExactlyOneRequired and MustDiffer.
- `errors/standalones/validation/mapper_validation_error.py`: define `MapperValidationError`
  and its `MapperValidationResultEmptyError` subtype. The base carries the mapper
  class and actual method; the subtype identifies empty output for assigned input.
- `errors/standalones/validation/function_validation_error.py`: define `FunctionValidationError`
  and `FunctionValidationNotImplementedError` in one module. The base carries
  read-only `owner_type` and `method` (`types.FunctionType`), identifying the
  responsible class and the unimplemented function without storing names or text.

```python
from framework_common.enums.enum_month import EnumMonth
from framework_common.enums.enum_timeframe import EnumTimeframe
from framework_common.errors.error_base import ErrorBase
from framework_common.errors.standalones.crawl.crawl_already_running_error import CrawlAlreadyRunningError
from framework_common.errors.standalones.validation.type_validation_error import TypeValidationError
from framework_common.errors.standalones.validation.value_validation_error import ValueValidationError
from framework_common.functions import function_enum
```

Applications can subclass `ErrorBase` for their own exception hierarchy.
Business-specific enums remain in the consuming application.

Organize error containers under `errors/containers/` and standalone errors by
capability under `errors/standalones/<capability>/`, matching application packages.
Import errors directly from their defining modules. `ErrorBase` and
`ContainerErrorBase` remain in `errors/error_base.py` and
`errors/container_error_base.py`; package initializers do not re-export classes.


`CrawlAlreadyRunningError(str_target)` carries a read-only `target`. Its class identifies
the failure; there is no separate code or user-facing message. Applications can
subclass it inside public error containers and fix the target in `__init__`.

`ContainerErrorBase` is the shared extension point for public error containers.
It exposes nested `TypeValidationError` and `ValueValidationError` entries that
inherit the implementations in `errors/standalones/validation/`. Derived application
containers reuse those entries without redeclaring them. The container itself
does not inherit `Exception` or `ErrorBase` and performs no validation.
Inherited entries have the same class identity across different containers;
use property metadata to identify the affected model and field.

`TypeValidationError` inherits `ErrorBase` and provides four read-only properties:
`field`, `expected_type`, `actual_type`, and `is_none_allowed`. `field` is the
original Python property descriptor or `inspect.Parameter`, not a string.
The constructor argument is named `field` for either form. Type properties contain class
objects. All constructor arguments are required, including `is_none_allowed`;
use `type(None)` as the actual type when
the rejected value is None. The error carries validation results; callers still
perform the type check. It has no user-facing message and does not inherit the
built-in `TypeError`.

```python
raise TypeValidationError(
    field=ExampleModel.name,
    typ_expected_type=str,
    typ_actual_type=int,
    bol_is_none_allowed=False,
)
```

`ExampleModel` represents an application model with a `name` property. Consumers
can use `error.field.fget.__name__` for a property getter or `error.field.name`
for a Parameter. Query/Update model type checks use Parameters identifying
`dm_query` and `dm_update`, with `DmAssignedBase` as the expected type.
Application containers inherit `ContainerErrorBase.TypeValidationError` for
every field. The constructor is inherited without overriding any defaults.

`ValueValidationError` provides read-only `field`, `expected_value` and
`actual_value`. Its three constructor arguments are required; None, False and 0
are retained as actual values, not treated as omitted. It does not infer a
comparison operator, execute validation or automatically serialize its values.
The application determines their meaning from the field and error subtype.
The value-validation base and single-field subtypes accept
`field: property | inspect.Parameter | tuple[inspect.Parameter, ...]`.
Use the original descriptor for model fields or a Parameter from
`inspect.signature(callable).parameters[name]` for function arguments. The
MustDiffer subtype accepts the same forms for `other_field` too. Property metadata
is available through `field.fget`; Parameter names through `field.name`. An ordered
Parameter tuple identifies a group of arguments; each position corresponds to
the same position in the grouped actual values. ExactlyOneRequired requires a
Parameter tuple and a matching tuple of presence flags.

Each subtype exposes its rule metadata, such as bounds, length unit, expected
format or the other property. Containers expose matching nested entries, all
catchable through their inherited `ValueValidationError`. Required errors have
no exact expected value; their subtype expresses the rule. `function_string.validate()`
and `function_integer.validate()` provide reusable checks without response messages.
Helpers are organized by data type alongside `function_enum`; no extension
classes or extension package are used.

Query and update inputs reuse `ValueValidationRequiredError` for None parameters
and `ValueValidationLengthError` for empty assigned fields (minimum 1, no maximum).
Length errors accept `maximum_length=None` to represent an unbounded maximum.
`MapperValidationResultEmptyError` inherits read-only `mapper_type` and `method`
(the actual function object) from `MapperValidationError`, identifying a broken
mapper output contract. Both classes are defined in the same module; callers
can catch the base to handle mapper-validation failures together.
There are no separate Query/Update Required error families. Application update
models define their writable fields; mappers do not repeat an unsupported-field
check or expose a separate error for it.

Service construction uses `ValueValidationExactlyOneRequiredError` when both the Session
factory and UoW are provided or both are absent. Its field is the ordered pair
of Parameters `(fnc_session_factory, uow)`, its actual value is their presence
pair, and its `expected_value` is the required supplied count, `1`. It stores
presence flags, not factory/UoW objects, and has no allowed-values list.
`ValueValidationNotAllowedError` remains for values outside a supplied allowed
list, such as unknown argument names or enum values. No service-configuration error family
is needed. Crawl-scope requirements retain their dedicated error.
`errors/standalones/crawl/crawl_sub_unit_of_work_not_allowed_error.py` defines
`CrawlSubUnitOfWorkNotAllowedError` for crawls that must own their commits and
cannot run within a child UoW. Applications expose it only in their crawl
containers, not in `ContainerErrorBase`.
Repository limits use the
same `ValueValidationRangeError` with an `inspect.Parameter` as its field. Framework's explicit
ValueError, TypeError, NotImplementedError and RuntimeError raises have been
replaced with structured custom errors. Interpreter- and library-generated
exceptions remain independent of these explicit validation checks.

```python
raise ValueValidationError(
    field=ExampleModel.status,
    value_expected="enabled",
    value_actual="disabled",
)
```

## API error codes

```python
from framework_common.enums.enum_api_error_code import EnumApiErrorCode
from framework_common.enums.enum_language import EnumLanguage

_enm_error: EnumApiErrorCode = EnumApiErrorCode.API_RETIRED
_str_code: str = _enm_error.value
_str_message_en: str = _enm_error.message_en
_str_message_zh_tw: str = _enm_error.message_zh_tw
_str_message_ko_kr: str = _enm_error.message_ko_kr
_str_message: str = _enm_error.get_message(EnumLanguage.KO_KR)
```

| Code | English message | Traditional Chinese message | Korean message |
| --- | --- | --- | --- |
| `API_RETIRED` | This API endpoint has been retired. | 此 API 端點已停止服務。 | 이 API 엔드포인트는 더 이상 제공되지 않습니다. |
| `TOKEN_INVALID` | Invalid authentication token. | 驗證權杖無效。 | 유효하지 않은 인증 토큰입니다. |

`EnumApiErrorCode` inherits the standard library Enum. Its public code values
intentionally use uppercase strings for frontend clients. All message properties
are read-only. `get_message(enm_language=EnumLanguage.EN_US)` selects the message
using the shared language Enum and defaults to English. Applications choose the
message language and HTTP status, and use
`.value` for the response code. These identifiers are not HTTP status codes or
internal exception types. Importing the Enum does not register exception handlers,
retire routes, validate tokens, or select a language from request headers.
