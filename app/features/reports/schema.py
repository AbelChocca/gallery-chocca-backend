from datetime import date

from pydantic import BaseModel

from app.features.inventory.types import (
    InventoryOwnerType
)

class GenerateInventoryMovementReportSchema(
    BaseModel
):
    owner_type: InventoryOwnerType

    start_date: date
    end_date: date