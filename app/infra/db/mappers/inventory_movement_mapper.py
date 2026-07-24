from app.infra.db.mappers.base_mapper import BaseMapper
from app.features.inventory.inventory_movement_entity import InventoryMovement
from app.features.inventory.models.inventory_movement import InventoryMovementTable

class InventoryMovementMapper(BaseMapper[InventoryMovement, InventoryMovementTable]):
    @staticmethod
    def to_db_model(entity: InventoryMovement, existing_model: InventoryMovementTable | None = None):
        if existing_model is not None:
            existing_model.new_stock = entity.new_stock
            existing_model.previous_stock = entity.previous_stock
            existing_model.location_id = entity.location_id
            existing_model.quantity = entity.quantity
            existing_model.reference_type=entity.reference_type
            existing_model.reference_id=entity.reference_id
            existing_model.reason = entity.reason
            existing_model.type = entity.type
            return existing_model
        return InventoryMovementTable(
            owner_name=entity.owner_name,
            owner_id=entity.owner_id,
            owner_code=entity.owner_code,
            location_id=entity.location_id,
            owner_type=entity.owner_type,
            type=entity.type,
            quantity=entity.quantity,
            previous_stock=entity.previous_stock,
            reference_type=entity.reference_type,
            reference_id=entity.reference_id,
            performed_by=entity.performed_by,
            new_stock=entity.new_stock,
            reason=entity.reason,
            created_at=entity.created_at
        )
    
    @staticmethod
    def to_entity(model: InventoryMovementTable):
        return InventoryMovement(
            owner_id=model.owner_id,
            owner_code=model.owner_code,
            owner_name=model.owner_name,
            owner_type=model.owner_type,
            location_id=model.location_id,
            reference_type=model.reference_type,
            reference_id=model.reference_id,
            performed_by=model.performed_by,
            type=model.type,
            quantity=model.quantity,
            previous_stock=model.previous_stock,
            new_stock=model.new_stock,
            reason=model.reason,
            id=model.id,
            created_at=model.created_at
        )

