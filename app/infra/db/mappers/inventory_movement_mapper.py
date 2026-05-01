from app.infra.db.mappers.base_mapper import BaseMapper
from app.domain.inventory.inventory_movement_entity import InventoryMovement
from app.infra.db.models.model_inventory_movement import InventoryMovementTable

class InventoryMovementMapper(BaseMapper[InventoryMovement, InventoryMovementTable]):
    @staticmethod
    def to_db_model(entity: InventoryMovement, existing_model: InventoryMovementTable | None = None):
        if existing_model is not None:
            existing_model.new_stock = entity.new_stock
            existing_model.previous_stock = entity.previous_stock
            existing_model.quantity = entity.quantity
            existing_model.reason = entity.reason
            existing_model.type = entity.type
            return existing_model
        return InventoryMovementTable(
            variant_size_id=entity.variant_size_id,
            type=entity.type,
            quantity=entity.quantity,
            previous_stock=entity.previous_stock,
            new_stock=entity.new_stock,
            reason=entity.reason,
            created_at=entity.created_at
        )
    
    @staticmethod
    def to_entity(model: InventoryMovementTable):
        return InventoryMovement(
            variant_size_id=model.variant_size_id,
            type=model.type,
            quantity=model.quantity,
            previous_stock=model.previous_stock,
            new_stock=model.new_stock,
            reason=model.reason,
            id=model.id,
            created_at=model.created_at
        )

