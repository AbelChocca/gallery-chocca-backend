from datetime import datetime, timezone

from app.features.material.entities.material import Material
from app.features.material.types import (
    MaterialType,
    UnitType,
)
from app.shared.types import CompanyType


def build_material(**overrides) -> Material:
    defaults = {
        "id": None,
        "code": "MAT-000001",
        "name": "Material",
        "description": "Material de prueba",
        "company": CompanyType.OLD_DENIM,
        "minimum_stock": 20,
        "material_type": MaterialType.FABRIC,
        "unit_type": UnitType.METER,
        "is_active": True,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    defaults.update(overrides)

    return Material(**defaults)