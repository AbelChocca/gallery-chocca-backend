from app.features.material.material_repository import (
    PostgresMaterialRepository
)
from app.shared.pagination.pagination_service import PaginationService
from app.features.material.entities.material import Material
from app.features.material.entities.material_component import MaterialComponent
from app.features.material.dto.material import (
    CreateMaterialDTO,
    UpdateMaterialDTO,
    MaterialFilters,
    MaterialPaginatedDTO,
    MaterialComponentDTO
)
from app.core.exceptions import ValidationError, ValueNotFound, InvalidOperation
from app.features.material.types import MaterialType
from decimal import Decimal

class MaterialService:
    def __init__(
        self,
        material_repository: PostgresMaterialRepository,
        pagination_service: PaginationService
    ):
        self._material_repository = material_repository
        self._pagination_service = pagination_service

    async def create(
        self,
        dto: CreateMaterialDTO
    ) -> Material:
        if await self._material_repository.exists_by_name(
            dto.name
        ):
            raise ValidationError(
                "Material name already exists.",
                {
                    "module_service": "material_service",
                    "repeated_name": dto.name
                }
            )
        
        components = None

        if dto.components:
            self._validate_components(dto, dto.material_type)
        
            components = [
                MaterialComponent(
                    id=None,
                    material_id=None,
                    fiber_type=component.fiber_type,
                    percentage=component.percentage,
                )
                for component in dto.components
            ]

        total_materials = (
            await self._material_repository.count_all()
        )

        sequence = total_materials + 1

        code = Material.build_code(
            dto.name,
            sequence
        )

        material = Material(
            id=None,
            code=code,
            name=dto.name,
            description=dto.description,
            company=dto.company,
            material_type=dto.material_type,
            unit_type=dto.unit_type,
            is_active=True,
            components=components,
        )

        return await self._material_repository.save(
            material
        )

    async def update(
        self,
        material_id: int,
        dto: UpdateMaterialDTO
    ) -> Material:
        material = await self._material_repository.get_by_id(
            material_id
        )

        if not material.is_active:
            raise InvalidOperation(
                "Cannot update material because it's disabled.",
                context={
                    "service": "material",
                    "material_id": material_id,
                    "material_name": material.name
                }
            )
        
        effective_material_type = (
            dto.material_type
            if dto.material_type is not None
            else material.material_type
        )

        if effective_material_type != MaterialType.FABRIC:
            if material.components:
                await self._material_repository.delete_components_by_material_id(
                    material.id
                )
                material.components = []

        elif dto.components is not None:
            self._validate_components(
                dto,
                effective_material_type
            )

            await self._material_repository.delete_components_by_material_id(
                material.id
            )

            material.components = [
                MaterialComponent(
                    id=None,
                    material_id=material.id,
                    fiber_type=c.fiber_type,
                    percentage=c.percentage,
                )
                for c in dto.components
            ]

        material.update_information(
            name=dto.name,
            description=dto.description,
            company=dto.company,
            material_type=dto.material_type,
            unit_type=dto.unit_type,
        )

        material.regenerate_code_prefix()

        material = await self._material_repository.save(
            material
        )

        return material

    async def get_components(
        self,
        *,
        material_id: int,
    ) -> list[MaterialComponentDTO]:

        components = await (
            self._material_repository
            .get_components_by_material_id(
                material_id=material_id,
            )
        )


        return [
            MaterialComponentDTO(
                id=component.id,
                material_id=component.material_id,
                fiber_type=component.fiber_type,
                percentage=component.percentage,
            )
            for component in components
        ]

    async def deactivate(
        self,
        material_id: int
    ) -> Material:

        material = await self._material_repository.get_by_id(
            material_id
        )

        material.deactivate()

        return await self._material_repository.save(
            material
        )

    async def activate(
        self,
        material_id: int
    ) -> Material:

        material = await self._material_repository.get_by_id(
            material_id
        )

        material.activate()

        return await self._material_repository.save(
            material
        )
    async def get_by_ids(
        self,
        ids: list[int]
    ) -> list[Material]:

        if not ids:
            return []

        return await self._material_repository.get_by_ids(ids)
    
    async def get_by_id(
        self,
        material_id: int
    ) -> Material:

        return await self._material_repository.get_by_id(
            material_id
        )

    async def get_all(
        self,
        *,
        filters: MaterialFilters | None = None,
        page: int = 1,
        limit: int = 20
    ) -> MaterialPaginatedDTO:

        offset = self._pagination_service.get_offset(
            page=page,
            limit=limit
        )

        total_items = await self._material_repository.count_all(
            filters=filters
        )

        materials = await self._material_repository.get_all(
            filters=filters,
            offset=offset,
            limit=limit
        )

        total_pages = (
            self._pagination_service.get_total_pages(
                total=total_items,
                limit=limit
            )
        )

        current_page = (
            self._pagination_service.get_current_page(
                offset,
                limit
            )
        )

        return MaterialPaginatedDTO.create(
            items=materials,
            total_items=total_items,
            current_page=current_page,
            total_pages=total_pages
        )
    
    def _validate_materials_found(
        self,
        requested_ids: list[int],
        materials: list[Material]
    ) -> None:
        if len(materials) != len(requested_ids):
            found_ids = {
                material.id
                for material in materials
            }

            missing_ids = [
                material_id
                for material_id in requested_ids
                if material_id not in found_ids
            ]

            raise ValueNotFound(
                "Some materials were not found.",
                {
                    "service": "material",
                    "event": "update_stock_many",
                    "missing_ids": missing_ids
                }
            )
        
    def _validate_components(
            self, 
            dto: CreateMaterialDTO | UpdateMaterialDTO,
            material_type: MaterialType   
        ):
        if dto.components and material_type != MaterialType.FABRIC:
            raise ValidationError(
                "Los componentes de un material no pueden asociarse a un material que no sea de tipo Tela.",
                {
                    "module_service": "material_service"
                }
            )
        
        for component in dto.components:
            if component.percentage <= Decimal("0"):
                raise ValidationError(
                    "Cada porcentaje debe ser mayor a 0.",
                    {
                        "module_service": "material_service"
                    }   
                )
        
        if len(dto.components) > 0:
            total = sum((c.percentage for c in dto.components), start=Decimal("0"))

            if total != Decimal("100"):
                raise ValidationError(
                    "La suma de los porcentajes de la composición debe ser exactamente 100%.",
                    {
                        "modele_service": "material_service"
                    }
                )
        
        fiber_types = [c.fiber_type for c in dto.components]

        if len(fiber_types) != len(set(fiber_types)):
            raise ValidationError(
                "No se pueden repetir tipos de fibra en la composición.",
                {
                    "modele_service": "material_service"
                }
            )