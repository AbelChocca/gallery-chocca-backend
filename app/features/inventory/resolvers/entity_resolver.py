from abc import ABC, abstractmethod

from app.features.inventory.dtos.inventory import InventoryOwnerDTO


class EntityResolver(ABC):

    @abstractmethod
    async def resolve(
        self,
        *,
        entity_id: int,
    ) -> InventoryOwnerDTO:
        ...