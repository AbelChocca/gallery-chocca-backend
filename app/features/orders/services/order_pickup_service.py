from datetime import datetime
from app.features.orders.entities.order_pickup import OrderPickup
from app.features.orders.repositories.order_pickup_repository import (
    OrderPickupRepository,
)


class OrderPickupService:

    def __init__(
        self,
        repository: OrderPickupRepository,
    ):
        self._repository = repository

    async def create(
        self,
        order_id: int,
        location_id: int,
        location_name: str,
        location_address: str,
        location_ubigeo_code: str,
        location_latitude: str,
        location_longitude: str,
        location_phone: str,
        location_reference: str,
        created_at: datetime | None = None,
    ) -> OrderPickup:
        order_pickup = OrderPickup(
            order_id=order_id,
            location_id=location_id,
            location_name=location_name,
            location_address=location_address,
            location_ubigeo_code=location_ubigeo_code,
            location_latitude=location_latitude,
            location_longitude=location_longitude,
            location_phone=location_phone,
            location_reference=location_reference,
            created_at=created_at,
        )
        return await self._repository.save(
            order_pickup,
            flush=True,
        )

    async def get_by_order_id(
        self,
        *,
        order_id: int,
    ) -> OrderPickup | None:
        return await self._repository.get_by_order_id(
            order_id=order_id,
        )
