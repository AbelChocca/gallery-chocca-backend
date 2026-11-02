from app.features.orders.entities.order_promotion import OrderPromotion
from app.features.orders.repositories.order_promotion_repository import (
    OrderPromotionRepository,
)


class OrderPromotionService:

    def __init__(
        self,
        repository: OrderPromotionRepository,
    ):
        self._repository = repository

    async def create(
        self,
        promotion: OrderPromotion,
    ) -> OrderPromotion:
        return await self._repository.save(promotion)

    async def create_all(
        self,
        promotions: list[OrderPromotion],
    ) -> list[OrderPromotion]:
        if not promotions:
            return []

        return await self._repository.save_all(promotions)

    async def get_by_order_id(
        self,
        order_id: int,
    ) -> list[OrderPromotion]:
        return await self._repository.get_by_order_id(
            order_id=order_id,
        )