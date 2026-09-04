from typing import Optional

from app.infra.db.mappers.base_mapper import BaseMapper
from app.features.balancing.models.inventory_valuation import (
    InventoryValuationTable,
)

from app.features.balancing.entities.inventory_valuation import (
    InventoryValuation,
)


class InventoryValuationMapper(
    BaseMapper[InventoryValuation, InventoryValuationTable]
):

    @staticmethod
    def to_entity(model: InventoryValuationTable) -> InventoryValuation:
        return InventoryValuation(
            id=model.id,
            balance_snapshot_id=model.balance_snapshot_id,
            category=model.category,
            subcategory=model.subcategory,
            description=model.description,
            brand=model.brand,
            location=model.location,
            quantity=model.quantity,
            unit_value=model.unit_value,
            updated_at=model.updated_at,
            created_at=model.created_at,
        )

    @staticmethod
    def to_db_model(
        entity: InventoryValuation,
        existing_model: Optional[InventoryValuationTable] = None,
    ) -> InventoryValuationTable:

        if existing_model:
            existing_model.balance_snapshot_id = entity.balance_snapshot_id
            existing_model.category = entity.category
            existing_model.subcategory = entity.subcategory
            existing_model.description = entity.description
            existing_model.brand = entity.brand
            existing_model.location = entity.location
            existing_model.quantity = entity.quantity
            existing_model.unit_value = entity.unit_value

            return existing_model

        return InventoryValuationTable(
            balance_snapshot_id=entity.balance_snapshot_id,
            category=entity.category,
            subcategory=entity.subcategory,
            description=entity.description,
            brand=entity.brand,
            location=entity.location,
            quantity=entity.quantity,
            unit_value=entity.unit_value,
            updated_at=entity.updated_at,
            created_at=entity.created_at,
        )