from app.features.material.types import (
    MaterialType, 
    UnitType
)
from app.shared.types import CompanyType
from datetime import datetime, timezone

from app.features.material.entities.material_component import MaterialComponent

class Material:
    def __init__(
        self,
        *,
        id: int | None,
        code: str,
        name: str,
        description: str | None,
        material_type: MaterialType,
        unit_type: UnitType,
        is_active: bool,
        company: CompanyType = CompanyType.OLD_DENIM,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        components: list[MaterialComponent] | None = None,
    ):
        self.id = id
        self.code = code
        self.name = name
        self.description = description
        self.company = company
        self.material_type = material_type
        self.unit_type = unit_type
        self.is_active = is_active
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)
        self.components = components or []

    def update_information(
        self,
        *,
        name: str | None = None,
        description: str | None = None,
        company: CompanyType | None = None,
        material_type: MaterialType | None = None,
        unit_type: UnitType | None = None,
    ) -> None:

        updated = False

        if name is not None and name != self.name:
            self.name = name
            updated = True

        if description is not None and description != self.description:
            self.description = description
            updated = True

        if company is not None and company != self.company:
            self.company = company
            updated = True

        if material_type is not None and material_type != self.material_type:
            self.material_type = material_type
            updated = True

        if unit_type is not None and unit_type != self.unit_type:
            self.unit_type = unit_type
            updated = True

        if updated:
            self._touch()

    def deactivate(self) -> None:
        self.is_active = False
        self._touch()

    def activate(self) -> None:
        self.is_active = True
        self._touch()

    @staticmethod
    def build_code(
        name: str,
        sequence: int
    ) -> str:
        prefix = "".join(
            word[0].upper()
            for word in name.split()
            if word.strip()
        )[:3]

        prefix = prefix.ljust(3, "X")

        return f"{prefix}-{sequence:06d}"
    
    def regenerate_code_prefix(
        self
    ) -> None:

        numeric_part = self.code.split("-")[1]

        prefix = "".join(
            word[0].upper()
            for word in self.name.split()
            if word.strip()
        )[:3]

        prefix = prefix.ljust(3, "X")

        self.code = f"{prefix}-{numeric_part}"

        self._touch()

    def _touch(self):
        self.updated_at = datetime.now(timezone.utc)