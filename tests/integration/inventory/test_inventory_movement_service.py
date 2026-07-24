import pytest

from app.features.inventory.types.inventory_movement import InventoryMovementType, InventoryOwnerType
from app.features.inventory.dtos.inventory_movements import InventoryMovementFilters
from app.features.inventory.services.inventory_movement_service import InventoryMovementService


@pytest.mark.asyncio
async def test_should_create_inventory_movement(
    inventory_movement_service: InventoryMovementService,
    location
):
    await inventory_movement_service.create_movement(
        movement_type=InventoryMovementType.ENTRY,
        owner_type=InventoryOwnerType.MATERIAL,
        location_id=location.id,
        owner_id=1,
        owner_name="Cemento",
        owner_code="MAT-001",
        quantity=10,
        prev_stock=20,
        new_stock=30,
        reason="Compra"
    )

    movement = await inventory_movement_service.get_movement_by_id(1)

    assert movement is not None
    assert movement.owner_name == "Cemento"
    assert movement.owner_code == "MAT-001"
    assert movement.quantity == 10
    assert movement.previous_stock == 20
    assert movement.new_stock == 30

@pytest.mark.asyncio
async def test_should_get_inventory_movements_filtered_and_paginated(
    inventory_movement_service: InventoryMovementService,
    location
):
    await inventory_movement_service.create_movement(
        movement_type=InventoryMovementType.ENTRY,
        owner_type=InventoryOwnerType.MATERIAL,
        owner_id=1,
        location_id=location.id,
        owner_name="Cemento",
        owner_code="MAT-001",
        quantity=10,
        prev_stock=20,
        new_stock=30,
        reason="Compra"
    )

    await inventory_movement_service.create_movement(
        movement_type=InventoryMovementType.SALE,
        owner_type=InventoryOwnerType.MATERIAL,
        owner_id=2,
        location_id=location.id,
        owner_name="Arena",
        owner_code="MAT-002",
        quantity=5,
        prev_stock=30,
        new_stock=25,
        reason="Venta"
    )

    result = await inventory_movement_service.get_paginated_inventory_movements(
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
    assert movement.type == InventoryMovementType.ENTRY

@pytest.mark.asyncio
async def test_should_get_last_material_movement(
    inventory_movement_service: InventoryMovementService,
    location,
):
    await inventory_movement_service.create_movement(
        movement_type=InventoryMovementType.ENTRY,
        owner_type=InventoryOwnerType.MATERIAL,
        owner_id=1,
        location_id=location.id,
        owner_name="Cemento",
        owner_code="MAT-001",
        quantity=10,
        prev_stock=0,
        new_stock=10,
        reason="Primera compra",
    )

    await inventory_movement_service.create_movement(
        movement_type=InventoryMovementType.MANUAL_ADJUSTMENT,
        owner_type=InventoryOwnerType.MATERIAL,
        owner_id=1,
        location_id=location.id,
        owner_name="Cemento",
        owner_code="MAT-001",
        quantity=5,
        prev_stock=10,
        new_stock=15,
        reason="Ajuste",
    )

    last_movement = (
        await inventory_movement_service.get_last_material_movement(
            owner_type=InventoryOwnerType.MATERIAL,
            owner_id=1,
        )
    )

    assert last_movement is not None
    assert last_movement.owner_id == 1
    assert last_movement.owner_type == InventoryOwnerType.MATERIAL
    assert last_movement.type == InventoryMovementType.MANUAL_ADJUSTMENT
    assert last_movement.previous_stock == 10
    assert last_movement.new_stock == 15
    assert last_movement.reason == "Ajuste"