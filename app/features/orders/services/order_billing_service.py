from app.features.orders.entities.order_billing import OrderBilling
from app.features.orders.repositories.order_billing_repository import (
    OrderBillingRepository,
)


class OrderBillingService:

    def __init__(
        self,
        repository: OrderBillingRepository,
    ):
        self._repository = repository

    async def create(
        self,
        billing: OrderBilling,
    ) -> OrderBilling:
        return await self._repository.save(billing)

    async def get_by_order_id(
        self,
        order_id: int,
        raises: bool = True,
    ) -> OrderBilling | None:
        return await self._repository.get_by_order_id(
            order_id=order_id,
            raises=raises,
        )