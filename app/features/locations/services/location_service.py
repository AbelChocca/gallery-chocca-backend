from datetime import datetime, timezone
from decimal import Decimal
from math import ceil

from app.core.exceptions import ValidationError

from app.features.locations.entities.location import Location
from app.features.locations.repositories.location_repository import (
    LocationRepository,
)
from app.features.locations.types import LocationType
from app.shared.pagination.dto import PaginatedDTO


class LocationService:

    def __init__(
        self,
        repository: LocationRepository,
    ):
        self._repository = repository

    async def get_by_id(
        self,
        *,
        location_id: int,
        raises: bool = False,
        with_lock: bool = False,
    ) -> Location | None:
        return await self._repository.get_by_id(
            model_id=location_id,
            raises=raises,
            with_lock=with_lock,
        )

    async def get_pickup_locations(self) -> list[Location]:
        return await self._repository.get_pickup_locations()

    async def get_pickup_location(
        self,
        *,
        location_id: int,
    ) -> Location:
        location = await self.get_by_id(
            location_id=location_id,
        )

        if location is None:
            raise ValidationError(
                message="La tienda seleccionada no existe."
            )

        if location.type != LocationType.STORE:
            raise ValidationError(
                message="La ubicación seleccionada no es una tienda."
            )

        if not location.is_active or not location.pickup_enabled:
            raise ValidationError(
                message="La tienda no está habilitada para recojo."
            )

        if not location.address or not location.ubigeo_code:
            raise ValidationError(
                message="La tienda no tiene una dirección de recojo válida."
            )

        return location

    
    async def set_active_status(
        self,
        *,
        location_id: int,
        is_active: bool,
    ) -> Location:

        location = await self.get_by_id(
            location_id=location_id,
            raises=True,
            with_lock=True,
        )

        location.is_active = is_active

        if not is_active:
            location.pickup_enabled = False

        location.updated_at = datetime.now(timezone.utc)

        return await self._repository.save(
            location,
            flush=True,
        )


    async def create(
        self,
        *,
        name: str,
        type: LocationType,
        address: str | None = None,
        ubigeo_code: str | None = None,
        latitude: Decimal | None = None,
        longitude: Decimal | None = None,
        phone: str | None = None,
        reference: str | None = None,
        external_provider: str | None = None,
        external_code: str | None = None,
        is_active: bool = True,
        pickup_enabled: bool = False,
    ) -> Location:

        self._validate_pickup_configuration(
            type=type,
            is_active=is_active,
            pickup_enabled=pickup_enabled,
            address=address,
            ubigeo_code=ubigeo_code,
        )

        now = datetime.now(timezone.utc)

        location = Location(
            name=name.strip(),
            type=type,
            address=address,
            ubigeo_code=ubigeo_code,
            latitude=latitude,
            longitude=longitude,
            phone=phone,
            reference=reference,
            external_provider=external_provider,
            external_code=external_code,
            is_active=is_active,
            pickup_enabled=pickup_enabled,
            created_at=now,
            updated_at=now,
        )

        return await self._repository.save(
            location,
            flush=True,
        )

    async def delete(
        self,
        *,
        location_id: int,
    ) -> None:

        location = await self.get_by_id(
            location_id=location_id,
            raises=True,
            with_lock=True,
        )

        # Baja lógica: mantiene los registros históricos.
        location.is_active = False
        location.pickup_enabled = False
        location.updated_at = datetime.now(timezone.utc)

        await self._repository.save(
            location,
            flush=True,
        )

    async def get_inventory_locations(
        self,
        *,
        search: str | None = None,
        is_active: bool | None = None,
    ) -> list[Location]:

        return await self._repository.get_inventory_locations(
            search=search,
            is_active=is_active,
        )

    async def get_locations(
        self,
        *,
        search: str | None = None,
        location_type: LocationType | None = None,
        is_active: bool | None = None,
        pickup_enabled: bool | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> PaginatedDTO[Location]:

        offset = (page - 1) * limit

        locations, total_items = (
            await self._repository.get_locations(
                search=search,
                location_type=location_type,
                is_active=is_active,
                pickup_enabled=pickup_enabled,
                offset=offset,
                limit=limit,
            )
        )

        total_pages = ceil(total_items / limit)

        return PaginatedDTO.create(
            items=locations,
            total_items=total_items,
            current_page=page,
            total_pages=total_pages,
        )

    @staticmethod
    def _validate_pickup_configuration(
        *,
        type: LocationType,
        is_active: bool,
        pickup_enabled: bool,
        address: str | None,
        ubigeo_code: str | None,
    ) -> None:

        if not pickup_enabled:
            return

        if type != LocationType.STORE:
            raise ValidationError(
                message=(
                    "Solo las ubicaciones de tipo STORE "
                    "pueden habilitar recojo."
                )
            )

        if not is_active:
            raise ValidationError(
                message=(
                    "Una ubicación inactiva no puede "
                    "habilitar recojo."
                )
            )

        if not address or not address.strip() or not ubigeo_code:
            raise ValidationError(
                message=(
                    "Las tiendas con recojo habilitado "
                    "requieren dirección y ubigeo."
                )
            )
