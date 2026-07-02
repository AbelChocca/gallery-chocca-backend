from abc import ABC, abstractmethod

from app.features.inventory.dto import (
    InventoryOwnerDTO,
    CreateBulkMovementCommand,
    UpdatedOwnerStockResult
)
from app.features.inventory.types import InventoryMovementType

class InventoryOwnerResolver(ABC):

    @abstractmethod
    async def update_stock(
        self,
        owner_id: int,
        quantity: int,
        movement_type: InventoryMovementType

    ) -> tuple[InventoryOwnerDTO, int]:
        """
        Returns:
            tuple[entity, previous_stock]
        """
        ...

    @abstractmethod
    async def update_stock_many(
        self,
        command: CreateBulkMovementCommand
    ) -> list[UpdatedOwnerStockResult]:
        ...

    @property
    @abstractmethod
    def cache_tag(self) -> str:
        ...