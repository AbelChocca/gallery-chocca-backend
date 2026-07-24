import pytest

from app.core.exceptions import (
    ValidationError,
    InvalidOperation,
)

from app.features.inventory.services.inventory_location_service import (
    InventoryLocationService,
)

from app.features.inventory.types.inventory_location import (
    InventoryLocationType,
)


async def test_create_location_success(
    inventory_location_service: InventoryLocationService,
):

    location = await inventory_location_service.create_location(
        name="  Tienda Gamarra  ",
        type=InventoryLocationType.STORE,
        address="  Lima  ",
    )

    assert location.id is not None
    assert location.name == "Tienda Gamarra"
    assert location.address == "Lima"
    assert location.is_active is True


async def test_create_location_empty_name(
    inventory_location_service: InventoryLocationService,
):

    with pytest.raises(
        ValidationError,
        match="The location name is required.",
    ):
        await inventory_location_service.create_location(
            name="   ",
            type=InventoryLocationType.STORE,
            address=None,
        )


async def test_create_location_duplicate_name(
    inventory_location_service: InventoryLocationService,
):

    await inventory_location_service.create_location(
        name="Tienda Centro",
        type=InventoryLocationType.STORE,
        address=None,
    )

    with pytest.raises(
        ValidationError,
        match="A location with this name already exists.",
    ):
        await inventory_location_service.create_location(
            name="Tienda Centro",
            type=InventoryLocationType.STORE,
            address=None,
        )

async def test_update_location_success(
    inventory_location_service: InventoryLocationService,
):

    location = await inventory_location_service.create_location(
        name="Tienda Vieja",
        type=InventoryLocationType.STORE,
        address="Lima",
    )


    updated = await inventory_location_service.update_location(
        location_id=location.id,
        name="Tienda Nueva",
        type=InventoryLocationType.WAREHOUSE,
        address="Surco",
        is_active=False,
    )

    assert updated.name == "Tienda Nueva"
    assert updated.type == InventoryLocationType.WAREHOUSE
    assert updated.address == "Surco"
    assert updated.is_active is False

async def test_update_location_duplicate_name(
    inventory_location_service: InventoryLocationService,
):

    first = await inventory_location_service.create_location(
        name="Tienda A",
        type=InventoryLocationType.STORE,
        address=None,
    )

    await inventory_location_service.create_location(
        name="Tienda B",
        type=InventoryLocationType.STORE,
        address=None,
    )


    with pytest.raises(
        ValidationError,
        match="A location with this name already exists.",
    ):
        await inventory_location_service.update_location(
            location_id=first.id,
            name="Tienda B",
            type=InventoryLocationType.STORE,
            address=None,
            is_active=True,
        )

async def test_toggle_location_deactivate_success(
    inventory_location_service: InventoryLocationService,
):

    location = await inventory_location_service.create_location(
        name="Tienda Test",
        type=InventoryLocationType.STORE,
        address=None,
    )

    await inventory_location_service.toggle_status(
        location_id=location.id,
        is_active=False,
    )

    updated = await inventory_location_service.get_location_by_id(
        location.id
    )

    assert updated.is_active is False

async def test_toggle_location_already_active(
    inventory_location_service: InventoryLocationService,
):

    location = await inventory_location_service.create_location(
        name="Tienda Test",
        type=InventoryLocationType.STORE,
        address=None,
    )


    with pytest.raises(
        InvalidOperation,
        match="Inventory location is already active.",
    ):
        await inventory_location_service.toggle_status(
            location_id=location.id,
            is_active=True,
        )

async def test_toggle_location_already_inactive(
    inventory_location_service: InventoryLocationService,
):

    location = await inventory_location_service.create_location(
        name="Tienda Test",
        type=InventoryLocationType.STORE,
        address=None,
    )

    await inventory_location_service.toggle_status(
        location_id=location.id,
        is_active=False,
    )


    with pytest.raises(
        InvalidOperation,
        match="Inventory location is already inactive.",
    ):
        await inventory_location_service.toggle_status(
            location_id=location.id,
            is_active=False,
        )