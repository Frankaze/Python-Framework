"""Reusable entity, repository, and transaction foundations."""

from framework_repository.entity_base import EntityBase
from framework_repository.repository_base import RepositoryBase
from framework_repository.unit_of_work import UnitOfWork

__all__: list[str] = ["EntityBase", "RepositoryBase", "UnitOfWork"]
