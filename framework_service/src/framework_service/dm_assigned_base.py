"""Track explicit field assignments independently from their values."""

from collections.abc import Mapping


class DmAssignedBase:
    """Distinguish an omitted field from a field explicitly assigned None."""

    # region Properties

    @property
    def assigned_fields(self) -> frozenset[str]:
        return frozenset(self._set_str_assigned_fields)

    # endregion Properties

    # region Constructor & Special Methods

    def __init__(self) -> None:
        self._set_str_assigned_fields: set[str] = set()

    # endregion Constructor & Special Methods

    # region Internal Methods

    def _assign_fields(
        self,
        dic_values: Mapping[str, object],
        dic_str_fields: Mapping[str, str],
    ) -> None:
        """Initialize only supplied arguments through the model's setters."""
        _set_unknown: set[str] = set(dic_values) - set(dic_str_fields)
        if _set_unknown:
            raise TypeError(
                "Unknown model arguments: " + ", ".join(sorted(_set_unknown))
            )
        _str_argument: str
        _value: object
        for _str_argument, _value in dic_values.items():
            setattr(self, dic_str_fields[_str_argument], _value)

    # endregion Internal Methods
