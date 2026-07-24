from typing import Optional

from app.features.inventory.entities.inventory_location import InventoryLocation
from app.features.inventory.models.inventory_location import (
    InventoryLocationTable,
)
from app.infra.db.mappers.base_mapper import BaseMapper


class InventoryLocationMapper(
    BaseMapper[InventoryLocation, InventoryLocationTable]
):
    @staticmethod
    def to_db_model(
        entity: InventoryLocation,
        existing_model: Optional[InventoryLocationTable] = None,
    ) -> InventoryLocationTable:
        model = existing_model or InventoryLocationTable()

        model.id = entity.id
        model.name = entity.name
        model.type = entity.type
        model.address = entity.address
        model.is_active = entity.is_active
        model.created_at = entity.created_at

        return model

    @staticmethod
    def to_entity(
        model: InventoryLocationTable,
    ) -> InventoryLocation:
        return InventoryLocation(
            id=model.id,
            name=model.name,
            type=model.type,
            address=model.address,
            is_active=model.is_active,
            created_at=model.created_at,
        )