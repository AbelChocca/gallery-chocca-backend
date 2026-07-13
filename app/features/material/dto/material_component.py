from dataclasses import dataclass
from decimal import Decimal

from app.features.material.entities.material_component import MaterialComponent
from app.features.material.types import FiberType


@dataclass(slots=True)
class MaterialComponentDTO:
    fiber_type: FiberType
    percentage: Decimal
    id: int | None = None
    material_id: int | None = None

    @classmethod
    def from_entity(
        cls,
        component: MaterialComponent
    ) -> "MaterialComponentDTO":
        return cls(
            id=component.id,
            material_id=component.material_id,
            fiber_type=component.fiber_type,
            percentage=component.percentage
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "material_id": self.material_id,
            "fiber_type": self.fiber_type.value,
            "percentage": str(self.percentage)
        }

    @classmethod
    def from_dict(
        cls,
        data: dict
    ) -> "MaterialComponentDTO":
        return cls(
            id=data["id"],
            material_id=data["material_id"],
            fiber_type=FiberType(data["fiber_type"]),
            percentage=Decimal(data["percentage"])
        )

@dataclass(slots=True)
class CreateMaterialComponentDTO:
    fiber_type: FiberType
    percentage: Decimal