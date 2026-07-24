from app.features.reports.builders.inventory_movement_report_builder import InventoryMovementReportBuilder
from app.features.inventory.services.inventory_movement_service import InventoryMovementService
from app.features.inventory.dependencies.services import get_inventory_service

from fastapi import Depends

def get_inventory_movement_report_builder(
    inventory_service: InventoryMovementService = Depends(get_inventory_service)
) -> InventoryMovementReportBuilder:
    return InventoryMovementReportBuilder(
        inventory_service=inventory_service
    )