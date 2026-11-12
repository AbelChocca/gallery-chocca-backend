from app.features.orders.entities.order_address import OrderAddress
from app.features.orders.repositories.order_address_repository import (
    OrderAddressRepository,
)


class OrderAddressService:

    def __init__(
        self,
        repository: OrderAddressRepository,
    ):
        self._repository = repository

    async def create(
        self,
        address: OrderAddress,
    ) -> OrderAddress:
        return await self._repository.save(address)

    async def get_by_order_id(
        self,
        order_id: int,
        raises: bool = True,
    ) -> OrderAddress | None:
        return await self._repository.get_by_order_id(
            order_id=order_id,
            raises=raises,
        )