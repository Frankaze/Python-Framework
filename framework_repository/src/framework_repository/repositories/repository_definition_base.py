"""Repository foundation for definition data identified by business keys."""

from framework_repository.models.entity_base import EntityBase
from framework_repository.repositories.repository_base import RepositoryBase


class RepositoryDefinitionBase[TEntity: EntityBase](RepositoryBase[TEntity]):
    """Extend common operations with application-specific business-key lookups."""
