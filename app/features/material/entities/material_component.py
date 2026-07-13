from decimal import Decimal

from app.features.material.types import FiberType


class MaterialComponent:
    def __init__(
        self,
        *,
        id: int | None,
        material_id: int | None,
        fiber_type: FiberType,
        percentage: Decimal,
    ):
        self.id = id
        self.material_id = material_id
        self.fiber_type = fiber_type
        self.percentage = percentage