
import pytest

from app.core.exceptions import ValidationError

from app.features.locations.services.location_service import LocationService
from app.features.locations.types import LocationType


pytestmark = pytest.mark.asyncio(
    loop_scope="session",
)


async def test_create_location_success(
    inventory_location_service: LocationService,
):
    location = await inventory_location_service.create(
        name="Tienda Gamarra",
        type=LocationType.STORE,
        address="Lima",
        is_active=True,
        pickup_enabled=False,
    )

    assert location.id is not None
    assert location.name == "Tienda Gamarra"
    assert location.type == LocationType.STORE
    assert location.address == "Lima"
    assert location.is_active is True


async def test_create_location_empty_name(
    inventory_location_service: LocationService,
):
    with pytest.raises(ValidationError):
        await inventory_location_service.create(
            name="   ",
            type=LocationType.STORE,
            address=None,
        )


async def test_create_location_duplicate_name(
    inventory_location_service: LocationService,
):
    await inventory_location_service.create(
        name="Tienda Centro",
        type=LocationType.STORE,
        address=None,
    )

    with pytest.raises(ValidationError):
        await inventory_location_service.create(
            name="Tienda Centro",
            type=LocationType.STORE,
            address=None,
        )


async def test_get_location_by_id_success(
    inventory_location_service: LocationService,
):
    created = await inventory_location_service.create(
        name="Tienda Principal",
        type=LocationType.STORE,
        address="Lima",
    )

    location = await inventory_location_service.get_by_id(
        location_id=created.id,
        raises=True,
    )

    assert location is not None
    assert location.id == created.id
    assert location.name == "Tienda Principal"


async def test_delete_location_success(
    inventory_location_service: LocationService,
):
    location = await inventory_location_service.create(
        name="Tienda Test",
        type=LocationType.STORE,
        address="Lima",
        is_active=True,
        pickup_enabled=False,
    )

    await inventory_location_service.delete(
        location_id=location.id,
    )

    updated = await inventory_location_service.get_by_id(
        location_id=location.id,
        raises=True,
    )

    assert updated.is_active is False
    assert updated.pickup_enabled is False


async def test_get_inactive_pickup_location(
    inventory_location_service: LocationService,
):
    location = await inventory_location_service.create(
        name="Tienda Inactiva",
        type=LocationType.STORE,
        address="Lima",
        is_active=False,
        pickup_enabled=False,
    )

    with pytest.raises(ValidationError):
        await inventory_location_service.get_pickup_location(
            location_id=location.id,
        )


async def test_get_warehouse_as_pickup_location(
    inventory_location_service: LocationService,
):
    location = await inventory_location_service.create(
        name="Almacen Central",
        type=LocationType.WAREHOUSE,
        address="Lima",
        is_active=True,
        pickup_enabled=False,
    )

    with pytest.raises(ValidationError):
        await inventory_location_service.get_pickup_location(
            location_id=location.id,
        )
