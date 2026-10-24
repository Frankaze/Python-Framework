"""Repository foundation for transaction data identified by integer IDs."""

from sqlalchemy.orm.interfaces import ORMOption

from framework_repository.entity_base import EntityBase
from framework_repository.repository_base import RepositoryBase


class RepositoryTransactionBase[TEntity: EntityBase](RepositoryBase[TEntity]):
    """Add integer primary-key access to the shared repository operations."""

    # region Public Methods

    def get_by_id(
        self, int_id: int, *, lst_ormo_options: list[ORMOption] | None = None
    ) -> TEntity | None:
        """Load by ID, refreshing cached entities when loader options are supplied."""
        return self._sqls.get(
            self._typ_entity,
            int_id,
            options=lst_ormo_options,
            populate_existing=bool(lst_ormo_options),
        )

    # endregion Public Methods
