import pytest

from app.features.inventory.types import InventoryMovementType, InventoryOwnerType
from app.features.inventory.dto import InventoryMovementFilters
from app.features.inventory.inventory_service import InventoryService


@pytest.mark.asyncio
async def test_should_create_inventory_movement(
    inventory_service: InventoryService
):
    await inventory_service.create_movement(
        movement_type=InventoryMovementType.RESTOCK,
        owner_type=InventoryOwnerType.MATERIAL,
        owner_id=1,
        owner_name="Cemento",
        owner_code="MAT-001",
        quantity=10,
        prev_stock=20,
        new_stock=30,
        reason="Compra"
    )

    movement = await inventory_service.get_movement_by_id(1)

    assert movement is not None
    assert movement.owner_name == "Cemento"
    assert movement.owner_code == "MAT-001"
    assert movement.quantity == 10
    assert movement.previous_stock == 20
    assert movement.new_stock == 30

@pytest.mark.asyncio
async def test_should_get_inventory_movements_filtered_and_paginated(
    inventory_service: InventoryService
):
    await inventory_service.create_movement(
        movement_type=InventoryMovementType.RESTOCK,
        owner_type=InventoryOwnerType.MATERIAL,
        owner_id=1,
        owner_name="Cemento",
        owner_code="MAT-001",
        quantity=10,
        prev_stock=20,
        new_stock=30,
        reason="Compra"
    )

    await inventory_service.create_movement(
        movement_type=InventoryMovementType.SALE,
        owner_type=InventoryOwnerType.MATERIAL,
        owner_id=2,
        owner_name="Arena",
        owner_code="MAT-002",
        quantity=5,
        prev_stock=30,
        new_stock=25,
        reason="Venta"
    )

    result = await inventory_service.get_paginated_inventory_movements(
        filter_command=InventoryMovementFilters(
            search="cement"
        ),
        page=1,
        limit=10
    )

    assert result.total_items == 1
    assert result.pagination.current_page == 1
    assert result.pagination.total_pages == 1

    assert len(result.items) == 1

    movement = result.items[0]

    assert movement.owner_name == "Cemento"
    assert movement.owner_code == "MAT-001"
    assert movement.type == InventoryMovementType.RESTOCK