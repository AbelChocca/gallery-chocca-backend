from app.features.orders.services.order_item_service import OrderItemService

from app.features.orders.services.order_service import OrderService

from app.features.customer.customer_service import CustomerService
from app.features.orders.types.order import GetMyOrderResult, GetMyOrderItemResult

from app.features.orders.entities.order_item import OrderItem

class GetMyOrdersUseCase:
    def __init__(
        self,
        *,
        customer_service: CustomerService,
        order_service: OrderService,
        order_item_service: OrderItemService,
    ) -> None:
        self._customer_service = customer_service
        self._order_service = order_service
        self._order_item_service = order_item_service

    async def execute(
        self,
        user_id: int | None,
        session_id: str | None,
    ) -> list[GetMyOrderResult]:
        customer = None

        if user_id is not None:
            customer = await self._customer_service.get_by_user_id(
                user_id,
            )

        elif session_id is not None:
            customer = await self._customer_service.get_by_session_id(
                session_id,
            )

        if customer is None:
            return []

        orders = await self._order_service.get_by_customer_id(
            customer.id,
        )

        if not orders:
            return []

        order_ids = [
            order.id
            for order in orders
        ]

        items = await self._order_item_service.get_by_order_ids(
            order_ids,
        )

        items_by_order_id: dict[int, list[OrderItem]] = {}

        for item in items:
            items_by_order_id.setdefault(
                item.order_id,
                [],
            ).append(item)

        return [
            GetMyOrderResult(
                id=order.id,
                order_number=order.order_number,
                status=order.status,
                subtotal=order.subtotal,
                discount_amount=order.discount_amount,
                shipping_cost=order.shipping_cost,
                total=order.total,
                items=[
                    GetMyOrderItemResult(
                        product_name=item.product_name,
                        color=item.color,
                        size=item.size,
                        quantity=item.quantity,
                        final_total=item.final_total,
                    )
                    for item in items_by_order_id.get(
                        order.id,
                        [],
                    )
                ],
            )
            for order in orders
        ]