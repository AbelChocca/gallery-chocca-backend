from decimal import Decimal
from datetime import datetime, timezone

from app.features.inventory.dtos.inventory import (
    ProductInventoryRowDTO,
    ProductInventoryDetailDTO,
    InventoryStockUpdateResult,
    MaterialInventoryRowDTO,
    MaterialInventoryDetailDTO
)
from app.features.inventory.dtos.inventory_movements import MovementItem
from app.features.inventory.types.inventory_movement import InventoryOwnerType, InventoryMovementType
from app.features.inventory.dtos.inventory_locations import InventoryLocationStockDTO
from app.features.material.types import MaterialType
from app.features.inventory.entities.inventory import Inventory
from app.features.inventory.types.inventory import (
    AvailabilityStatus,
)
from app.features.inventory.repositories.inventory_repository import (
    InventoryRepository,
)
from app.features.inventory.strategy.registry import (
    get_inventory_strategy,
)

from app.core.exceptions import (
    InvalidOperation,
    ValueNotFound,
)

class InventoryService:

    def __init__(
        self,
        inventory_repository: InventoryRepository,
    ) -> None:
        self._inventory_repository = inventory_repository

    async def get_inventory_material_detail(
        self,
        *,
        material_id: int,
    ) -> MaterialInventoryDetailDTO:

        material = await (
            self._inventory_repository
            .get_inventory_material_detail(
                material_id=material_id,
            )
        )


        return MaterialInventoryDetailDTO(
            material_id=material["material_id"],

            code=material["code"],
            name=material["name"],

            description=material["description"],

            company=material["company"],
            material_type=material["material_type"],
            unit_type=material["unit_type"],

            image_url=None,

            total_quantity=material["total_quantity"],
            total_reserved_quantity=(
                material["total_reserved_quantity"]
            ),

            total_available_quantity=(
                material["total_available_quantity"]
            ),

            minimum_stock=material["minimum_stock"],

            availability_status=(
                material["availability_status"]
            ),

            is_active=material["is_active"],

            created_at=material["created_at"],
            updated_at=material["updated_at"],

            components=[],
            locations=[],
        )

    async def update_stock(
        self,
        *,
        owner_type: InventoryOwnerType,
        owner_id: int,
        location_id: int,
        quantity: Decimal,
        movement_type: InventoryMovementType,
    ):

        inventory = await self._inventory_repository.get_by_owner_location(
            owner_type=owner_type,
            owner_id=owner_id,
            location_id=location_id,
        )

        if inventory is None:
            return None

        previous_stock = inventory.quantity

        strategy = get_inventory_strategy(
            movement_type
        )

        new_stock = strategy.compute_new_stock(
            current_stock=inventory.quantity,
            quantity=quantity,
        )

        inventory.quantity = new_stock

        await self._inventory_repository.update_stock(
            inventory_id=inventory.id,
            new_stock=new_stock,
        )

        return InventoryStockUpdateResult(
            location_id=inventory.location_id,
            owner_id=inventory.owner_id,
            previous_stock=previous_stock,
            current_stock=new_stock
        )

    async def update_stock_many(
        self,
        *,
        owner_type: InventoryOwnerType,
        movement_type: InventoryMovementType,
        movement_items: list[MovementItem],
    ) -> list[InventoryStockUpdateResult]:

        owner_ids = [
            item.owner_id
            for item in movement_items
        ]

        inventories = await self._inventory_repository.get_owner_inventories_many(
            owner_type=owner_type,
            owner_ids=owner_ids,
        )

        inventories_by_owner = {
            inventory.owner_id: inventory
            for inventory in inventories
        }

        self._validate_inventories_found(
            owner_ids,
            inventories_by_owner
        )


        strategy = get_inventory_strategy(
            movement_type
        )


        stock_updates = {}

        results = []


        for item in movement_items:

            inventory = inventories_by_owner[
                item.owner_id
            ]

            previous_stock = inventory.quantity


            new_stock = strategy.compute_new_stock(
                current_stock=inventory.quantity,
                quantity=item.quantity,
            )


            inventory.quantity = new_stock


            stock_updates[inventory.id] = {
                "quantity": new_stock,
            }


            results.append(
                InventoryStockUpdateResult(
                    owner_id=inventory.owner_id,
                    location_id=inventory.location_id,
                    previous_stock=previous_stock,
                    current_stock=new_stock,
                )
            )


        await self._inventory_repository.update_stock_many(
            stock_updates
        )


        return results

    async def get_owner_inventories(
        self,
        *,
        owner_id: int,
        owner_type: InventoryOwnerType
    ) -> list[Inventory]:

        return await self._inventory_repository.get_owner_inventories(
            owner_id=owner_id,
            owner_type=owner_type
        )

    async def get_owner_inventory_locations(
        self,
        *,
        owner_type: InventoryOwnerType,
        owner_id: int,
    ) -> list[InventoryLocationStockDTO]:

        rows = await (
            self._inventory_repository
            .get_inventory_owner_locations(
                owner_type=owner_type,
                owner_id=owner_id,
            )
        )


        return [
            InventoryLocationStockDTO(
                inventory_id=row.inventory_id,

                location_id=row.location_id,
                location_name=row.location_name,
                location_type=row.location_type,

                quantity=row.quantity,
                reserved_quantity=row.reserved_quantity,

                available_quantity=(
                    row.quantity -
                    row.reserved_quantity
                ),

                minimum_stock=row.minimum_stock,

                address=row.location_address,

                availability_status=self._calculate_status(
                    row.quantity -
                    row.reserved_quantity,
                    row.minimum_stock,
                ),

                last_movement_at=row.last_movement_at,
            )
            for row in rows
            if row.inventory_id is not None
        ]
    
    async def update_minimum_stock(
        self,
        *,
        inventory_id: int,
        minimum_stock: Decimal,
    ) -> None:

        if minimum_stock < Decimal("0"):
            raise InvalidOperation(
                "Minimum stock cannot be negative."
            )

        await self._inventory_repository.update_minimum_stock(
            inventory_id=inventory_id,
            minimum_stock=minimum_stock,
        )
    
    async def delete_inventory(
        self,
        *,
        inventory_id: int,
    ) -> None:

        inventory = await self._inventory_repository.get_by_id(
            model_id=inventory_id,
            raises=False,
        )

        if inventory is None:
            raise ValueNotFound(
                "Inventory not found."
            )

        if inventory.quantity > Decimal("0"):
            raise InvalidOperation(
                "Cannot remove an inventory that still contains stock."
            )

        if inventory.reserved_quantity > Decimal("0"):
            raise InvalidOperation(
                "Cannot remove an inventory that still contains reserved stock."
            )

        await self._inventory_repository.delete_by_id(
            model_id=inventory_id,
        )

    async def create_inventory(
        self,
        *,
        owner_type: InventoryOwnerType,
        owner_id: int,
        location_id: int,
        minimum_stock: Decimal = Decimal("0"),
    ) -> Inventory:

        if minimum_stock < Decimal("0"):
            raise InvalidOperation(
                "Minimum stock cannot be negative"
            )

        inventory = Inventory(
            owner_type=owner_type,
            owner_id=owner_id,
            location_id=location_id,
            quantity=Decimal("0"),
            reserved_quantity=Decimal("0"),
            minimum_stock=minimum_stock,
            last_movement_at=None
            )

        return await self._inventory_repository.save(
            inventory
        )

    async def create_inventory_with_stock(
        self,
        *,
        owner_type: InventoryOwnerType,
        owner_id: int,
        location_id: int,
        quantity: Decimal,
        minimum_stock: Decimal = Decimal("0"),
        last_movement_at: datetime | None = None,
    ) -> Inventory:

        if quantity < Decimal("0"):
            raise InvalidOperation(
                "Quantity cannot be negative"
            )

        if minimum_stock < Decimal("0"):
            raise InvalidOperation(
                "Minimum stock cannot be negative"
            )

        inventory = Inventory(
            owner_type=owner_type,
            owner_id=owner_id,
            location_id=location_id,
            quantity=quantity,
            reserved_quantity=Decimal("0"),
            minimum_stock=minimum_stock,
            last_movement_at=(
            last_movement_at
            or datetime.now(timezone.utc)
        ),
        )

        inventory = await self._inventory_repository.save(
            inventory
        )

        return InventoryStockUpdateResult(
            owner_id=inventory.owner_id,
            location_id=location_id,
            previous_stock=Decimal("0"),
            current_stock=inventory.quantity,
        )

    async def get_inventory_materials(
        self,
        *,
        current_location_id: int,
        offset: int = 0,
        limit: int = 20,
        search: str | None = None,
        material_type: MaterialType | None = None,
        availability_status: AvailabilityStatus | None = None,
        is_active: bool | None = None,
    ) -> list[MaterialInventoryRowDTO]:

        rows = await self._inventory_repository.get_inventory_materials(
            current_location_id=current_location_id,
            offset=offset,
            limit=limit,
            search=search,
            material_type=material_type,
            availability_status=availability_status,
            is_active=is_active,
        )

        return [
            MaterialInventoryRowDTO(
                material_id=row.material_id,

                code=row.code,
                name=row.name,

                material_type=row.material_type,
                unit_type=row.unit_type,
                is_active=row.is_active,

                image_url=None,

                minimum_stock=row.minimum_stock,

                total_quantity=row.total_quantity,
                reserved_quantity=row.reserved_quantity,
                available_quantity=row.available_quantity,

                availability_status=row.availability_status,
            )
            for row in rows
        ]

    async def get_inventory_materials_count(
        self,
        *,
        current_location_id: int,
        search: str | None = None,
        material_type: MaterialType | None = None,
        availability_status: AvailabilityStatus | None = None,
        is_active: bool | None = None,
    ) -> int:
        return await self._inventory_repository.get_inventory_materials_count(
            current_location_id=current_location_id,
            search=search,
            material_type=material_type,
            availability_status=availability_status,
            is_active=is_active
        )
    
    async def get_inventory_products(
        self,
        *,
        offset: int = 0,
        limit: int = 20,
        current_location_id: int,
        search: str | None = None,
        colors: list[str] | None = None,
        size: str | None = None,
    ) -> list[ProductInventoryRowDTO]:

        rows = await self._inventory_repository.get_inventory_products(
            offset=offset,
            limit=limit,
            search=search,
            colors=colors,
            size=size,
        )

        variant_size_ids = [
            row.variant_size_id
            for row in rows
        ]

        other_locations_stock = await (
            self._inventory_repository.get_other_locations_stock(
                owner_ids=variant_size_ids,
                owner_type=InventoryOwnerType.PRODUCT,
                current_location_id=current_location_id,
            )
        )

        return [
            self._to_inventory_row_dto(
                row=row,
                other_locations_stock=other_locations_stock,
            )
            for row in rows
        ]
    
    async def validate_location_has_no_stock(
        self,
        *,
        location_id: int,
    ) -> None:

        has_stock = await self._inventory_repository.has_stock_in_location(
            location_id=location_id,
        )

        if has_stock:
            raise InvalidOperation(
                "Cannot deactivate an inventory location that still contains stock."
            )

    async def get_inventory_products_count(
        self,
        *,
        search: str | None = None,
        colors: list[str] | None = None,
        size: str |None = None,
    ) -> int:

        return await self._inventory_repository.get_inventory_products_count(
            search=search,
            colors=colors,
            size=size,
        )

    async def get_inventory_product_detail(
        self,
        *,
        variant_size_id: int,
    ) -> ProductInventoryDetailDTO:

        rows = await (
            self._inventory_repository
            .get_inventory_product_detail(
                variant_size_id=variant_size_id,
            )
        )

        if not rows:
            raise ValueNotFound(
                "Inventory product detail not found."
            )

        first = rows[0]

        locations: list[InventoryLocationStockDTO] = []

        total_quantity = Decimal("0")
        total_reserved_quantity = Decimal("0")
        total_minimum_stock = Decimal("0")


        for row in rows:

            if row.inventory_id is None:
                continue


            available_quantity = (
                row.quantity -
                row.reserved_quantity
            )

            total_quantity += row.quantity
            total_reserved_quantity += row.reserved_quantity
            total_minimum_stock += row.minimum_stock


            locations.append(
                InventoryLocationStockDTO(
                    inventory_id=row.inventory_id,

                    location_id=row.location_id,
                    location_name=row.location_name,
                    location_type=row.location_type,

                    quantity=row.quantity,
                    reserved_quantity=row.reserved_quantity,
                    available_quantity=available_quantity,

                    minimum_stock=row.minimum_stock,

                    address=row.location_address,

                    availability_status=self._calculate_status(
                        available_quantity,
                        row.minimum_stock,
                    ),

                    last_movement_at=row.last_movement_at,
                )
            )


        total_available_quantity = (
            total_quantity -
            total_reserved_quantity
        )


        return ProductInventoryDetailDTO(
            variant_size_id=first.variant_size_id,
            variant_id=first.variant_id,

            name=first.nombre,

            color=first.color,
            size=first.size,

            sku=first.sku,
            barcode=first.barcode,

            image_url=None,

            total_quantity=total_quantity,
            total_reserved_quantity=total_reserved_quantity,
            total_available_quantity=total_available_quantity,

            total_minimum_stock=total_minimum_stock,

            availability_status=self._calculate_status(
                total_available_quantity,
                total_minimum_stock,
            ),

            locations=locations,
        )

    def _to_inventory_row_dto(
        self,
        *,
        row,
        other_locations_stock: dict[int, Decimal],
    ) -> ProductInventoryRowDTO:
        
        available_quantity = row.total_quantity - row.reserved_quantity
        
        other_quantity = other_locations_stock.get(
            row.variant_size_id,
            Decimal("0")
        )

        return ProductInventoryRowDTO(
            variant_size_id=row.variant_size_id,
            variant_id=row.variant_id,

            name=row.nombre,

            color=row.color,
            size=row.size,

            sku=row.sku,
            barcode=row.barcode,

            image_url=None,

            available_quantity=available_quantity,
            total_quantity=row.total_quantity,
            reserved_quantity=row.reserved_quantity,
            total_minimum_stock=row.total_minimum_stock,

            availability_status=self._calculate_status(
                available_quantity,
                row.total_minimum_stock,
            ),

             has_stock_in_other_locations=(
                other_quantity > Decimal("0")
            ),

            other_locations_total_quantity=other_quantity,
        )


    def _calculate_status(
        self,
        quantity: Decimal,
        minimum_stock: Decimal
    ) -> AvailabilityStatus:

        if quantity == Decimal("0"):
            return AvailabilityStatus.OUT_OF_STOCK

        if quantity <= minimum_stock:
            return AvailabilityStatus.CRITICAL

        return AvailabilityStatus.AVAILABLE

    def _validate_inventories_found(
        self,
        requested_ids,
        inventories_by_owner
    ):
        missing = [
            id
            for id in requested_ids
            if id not in inventories_by_owner
        ]

        if missing:
            raise ValueNotFound(
                "Some materials were not found.",
                {
                    "service": "material",
                    "event": "update_stock_many",
                    "missing_ids": missing
                }
            )