from app.infra.db.repositories.material_repository import (
    PostgresMaterialRepository
)
from app.shared.pagination.pagination_service import PaginationService
from app.features.material.entity import Material
from app.features.material.dto import (
    CreateMaterialDTO,
    UpdateMaterialDTO,
    MaterialFilters,
    MaterialPaginatedDTO
)
from app.features.inventory.types import InventoryMovementType
from app.features.inventory.dto import MovementItem
from app.core.exceptions import ValidationError, ValueNotFound
from app.features.inventory.strategy.registry import get_inventory_strategy


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
            minimum_stock=dto.minimum_stock,
            company=dto.company,
            material_type=dto.material_type,
            unit_type=dto.unit_type,
            is_active=True
        )

        return await self._material_repository.save(
            material
        )

    async def update(
        self,
        material_id: int,
        dto: UpdateMaterialDTO
    ) -> None:

        material = await self._material_repository.get_by_id(
            material_id
        )

        material.update_information(
            name=dto.name,
            description=dto.description,
            company=dto.company,
            material_type=dto.material_type,
            unit_type=dto.unit_type,
            minimum_stock=dto.minimum_stock
        )

        material.regenerate_code_prefix()

        await self._material_repository.save(
            material
        )

        return None
    
    async def update_stock(
        self,
        material_id: int,
        quantity: int,
        movement_type: InventoryMovementType
    ) -> tuple[Material, int]:

        material = await self.get_by_id(material_id)

        previous_stock = material.stock

        strategy = get_inventory_strategy(
            movement_type
        )

        new_stock = strategy.compute_new_stock(
            current_stock=material.stock,
            quantity=quantity
        )
        material.stock = new_stock

        await self._material_repository.update_stock(
            material_id=material.id,
            new_stock=new_stock
        )

        return material, previous_stock
    
    async def update_stock_many(
        self,
        material_ids: list[int],
        movement_type: InventoryMovementType,
        movement_items: list[MovementItem]

    ) -> list[tuple[Material, int]]:

        materials = await self._material_repository.get_by_ids(
            material_ids
        )

        self._validate_materials_found(
            material_ids,
            materials
        )

        materials_by_id = {
            material.id: material
            for material in materials
        }

        strategy = get_inventory_strategy(
            movement_type
        )

        stock_updates: dict[int, int] = {}
        result: list[tuple[Material, int]] = []

        for item in movement_items:

            material = materials_by_id[item.owner_id]

            previous_stock = material.stock

            new_stock = strategy.compute_new_stock(
                current_stock=material.stock,
                quantity=item.quantity
            )

            stock_updates[material.id] = new_stock
            material.stock = new_stock

            result.append(
                (material, previous_stock)
            )

        await self._material_repository.update_stock_many(
            stock_updates
        )

        return result

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