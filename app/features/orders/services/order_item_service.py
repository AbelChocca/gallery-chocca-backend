from app.features.orders.entities.order_item import OrderItem
from app.features.orders.repositories.order_item_repository import (
    OrderItemRepository,
)


class OrderItemService:

    def __init__(
        self,
        repository: OrderItemRepository,
    ):
        self._repository = repository

    async def get_by_order_ids(
        self,
        order_ids: list[int],
    ) -> list[OrderItem]:
        return await self._repository.get_by_order_ids(
            order_ids,
        )

    async def create(
        self,
        item: OrderItem,
    ) -> OrderItem:
        return await self._repository.save(item)

    async def create_all(
        self,
        items: list[OrderItem],
    ) -> list[OrderItem]:
        return await self._repository.save_all(items)

    async def get_by_order_id(
        self,
        order_id: int,
    ) -> list[OrderItem]:
        return await self._repository.get_by_order_id(
            order_id=order_id,
        )