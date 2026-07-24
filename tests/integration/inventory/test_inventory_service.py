from app.features.inventory.services.inventory_service import InventoryService
from app.core.exceptions import InvalidOperation, ValueNotFound
from app.features.inventory.types.inventory import AvailabilityStatus

import pytest
from decimal import Decimal


async def test_create_inventory_success(
    inventory_service: InventoryService,
    variant_size,
    location,
):
    inventory = await inventory_service.create_inventory(
        variant_size_id=variant_size.id,
        location_id=location.id,
        minimum_stock=Decimal("5"),
    )

    assert inventory.id is not None
    assert inventory.quantity == Decimal("0")
    assert inventory.reserved_quantity == Decimal("0")
    assert inventory.minimum_stock == Decimal("5")


async def test_create_inventory_negative_minimum(
    inventory_service,
    variant_size,
    location,
):
    with pytest.raises(
        InvalidOperation,
        match="Minimum stock cannot be negative",
    ):
        await inventory_service.create_inventory(
            variant_size_id=variant_size.id,
            location_id=location.id,
            minimum_stock=Decimal("-1"),
        )


async def test_update_minimum_stock(
    inventory_service: InventoryService,
    variant_size,
    location,
):
    inventory = await inventory_service.create_inventory(
        variant_size_id=variant_size.id,
        location_id=location.id,
        minimum_stock=Decimal("2"),
    )

    updated = await inventory_service.update_minimum_stock(
        inventory_id=inventory.id,
        minimum_stock=Decimal("10"),
    )

    inventory = await inventory_service._inventory_repository.get_by_id(inventory.id)

    assert inventory.minimum_stock == Decimal("10")


async def test_update_minimum_stock_negative(
    inventory_service,
):
    with pytest.raises(
        InvalidOperation,
        match="Minimum stock cannot be negative.",
    ):
        await inventory_service.update_minimum_stock(
            inventory_id=1,
            minimum_stock=Decimal("-1"),
        )


async def test_delete_inventory(
    inventory_service: InventoryService,
    variant_size,
    location,
):
    inventory = await inventory_service.create_inventory(
        variant_size_id=variant_size.id,
        location_id=location.id,
    )

    await inventory_service.delete_inventory(
        inventory_id=inventory.id,
    )

    deleted = await inventory_service._inventory_repository.get_by_id(
        model_id=inventory.id,
        raises=False
    )

    assert deleted is None


async def test_delete_inventory_with_stock(
    inventory_service: InventoryService,
    variant_size,
    location,
):
    inventory = await inventory_service.create_inventory(
        variant_size_id=variant_size.id,
        location_id=location.id,
    )

    inventory.quantity = Decimal("5")

    await inventory_service._inventory_repository.save(
        inventory,
    )

    with pytest.raises(
        InvalidOperation,
        match="Cannot remove an inventory that still contains stock.",
    ):
        await inventory_service.delete_inventory(
            inventory_id=inventory.id,
        )


def test_calculate_status_available(
    inventory_service: InventoryService,
):
    assert (
        inventory_service._calculate_status(
            Decimal("10"),
            Decimal("5"),
        )
        == AvailabilityStatus.AVAILABLE
    )


async def test_delete_inventory_not_found(
    inventory_service: InventoryService,
):
    with pytest.raises(
        ValueNotFound,
        match="Inventory not found.",
    ):
        await inventory_service.delete_inventory(
            inventory_id=999999,
        )