"""Shared entity foundation without an application-owned ORM registry."""


class EntityBase:
    """Combine with DeclarativeBase in each application to isolate its mappings.

    This mixin does not create a registry, metadata, or mapped tables itself.
    Application entity bases supply those through SQLAlchemy DeclarativeBase.
    """
