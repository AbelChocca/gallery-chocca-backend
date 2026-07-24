from app.features.inventory.entities.inventory import Inventory
from app.features.inventory.models.inventory import InventoryTable
from app.infra.db.mappers.base_mapper import BaseMapper


class InventoryMapper(BaseMapper[Inventory, InventoryTable]):

    @staticmethod
    def to_db_model(
        entity: Inventory,
        existing_model: InventoryTable | None = None,
    ) -> InventoryTable:

        model = existing_model or InventoryTable()

        model.id = entity.id

        model.owner_type = entity.owner_type
        model.owner_id = entity.owner_id

        model.location_id = entity.location_id

        model.quantity = entity.quantity
        model.reserved_quantity = entity.reserved_quantity
        model.minimum_stock = entity.minimum_stock

        model.last_movement_at = entity.last_movement_at

        return model

    @staticmethod
    def to_entity(
        model: InventoryTable,
    ) -> Inventory:

        return Inventory(
            id=model.id,

            owner_type=model.owner_type,
            owner_id=model.owner_id,

            location_id=model.location_id,

            quantity=model.quantity,
            reserved_quantity=model.reserved_quantity,
            minimum_stock=model.minimum_stock,

            last_movement_at=model.last_movement_at,
        )