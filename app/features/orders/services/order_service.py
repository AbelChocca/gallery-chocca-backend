from app.features.orders.entities.order import Order
from app.features.orders.repositories.order_repository import (
    OrderRepository,
)
from app.features.orders.types.order import OrderStatus, AdminOrderListItemDTO, OrderFilters, UpdateOrderShippingResult
from app.shared.pagination.pagination_service import PaginationService
from app.shared.pagination.dto import PaginatedDTO
from app.core.exceptions import ValidationError
from app.features.payments.types.payment import PaymentMethod
from app.features.orders.types.delivery import DeliveryMethod
from app.core.exceptions import InvalidOperation

from decimal import Decimal
from datetime import datetime, timezone, timedelta

class OrderService:

    def __init__(
        self,
        repository: OrderRepository,
        pagination_service: PaginationService,
    ):
        self._repository = repository
        self.pagination_service = pagination_service

    async def cancel_expired_orders(
        self,
        *,
        flush: bool = True,
    ) -> list[Order]:
        now = datetime.now(timezone.utc)

        expired_before = (
            now - timedelta(hours=24)
        )

        orders = await (
            self._repository
            .get_expired_pending_orders(
                expired_before=expired_before,
                with_lock=True,
            )
        )

        if not orders:
            return []

        for order in orders:
            order.status = (
                OrderStatus.CANCELLED
            )

            order.updated_at = now

        return await self._repository.save_all(
            orders,
            flush=flush,
        )

    async def cancel_expired_order_by_id(
        self,
        *,
        order_id: int,
        flush: bool = True,
    ) -> Order:
        order = await self.get_by_id(
            order_id=order_id,
            raises=True,
            with_lock=True,
        )

        if order.status != OrderStatus.PENDING_PAYMENT:
            raise InvalidOperation(
                message=(
                    "Solo se pueden cancelar por expiración "
                    "pedidos pendientes de pago."
                ),
            )

        now = datetime.now(
            timezone.utc
        )

        expires_at = (
            order.created_at
            + timedelta(hours=24)
        )

        if now < expires_at:
            raise InvalidOperation(
                message=(
                    "El pedido todavía no ha superado "
                    "las 24 horas pendientes de pago."
                ),
            )

        order.status = (
            OrderStatus.CANCELLED
        )

        order.updated_at = now

        return await self._repository.save(
            order,
            flush=flush,
        )

    async def update_status(
        self,
        *,
        order_id: int,
        status: OrderStatus,
        flush: bool = True,
    ) -> Order:

        order = await self._repository.get_by_id(
            order_id,
            with_lock=True
        )

        if order is not None:
            order.status = status
            order.updated_at = datetime.now(
                timezone.utc
            )

            return await self._repository.save(
                order,
                flush=flush,
            )

    async def get_admin_orders(
        self,
        *,
        filters: OrderFilters,
        page: int,
        limit: int,
    ) -> PaginatedDTO[
        AdminOrderListItemDTO
    ]:
        offset = (
            self.pagination_service.get_offset(
                page=page,
                limit=limit,
            )
        )

        items, total_items = (
            await self._repository.get_admin_orders(
                filters=filters,
                offset=offset,
                limit=limit,
            )
        )

        total_pages = (
            self.pagination_service.get_total_pages(
                total=total_items,
                limit=limit,
            )
        )

        current_page = (
            self.pagination_service.get_current_page(
                offset=offset,
                limit=limit,
            )
        )

        return PaginatedDTO.create(
            items=items,
            total_items=total_items,
            current_page=current_page,
            total_pages=total_pages,
        )

    async def create(
        self,
        *,
        customer_id: int,
        subtotal: Decimal,
        discount_amount: Decimal,
        shipping_cost: Decimal,
        payment_method: PaymentMethod,
        delivery_method: DeliveryMethod,
        total: Decimal,
        now: datetime,
    ) -> Order:
        sequence = await self._repository.next_order_sequence()

        order_number = f"GC-{now.year}-{sequence:06d}"

        order = Order(
            order_number=order_number,
            customer_id=customer_id,
            status=OrderStatus.PENDING_PAYMENT,
            delivery_method=delivery_method,
            payment_method=payment_method,
            subtotal=subtotal,
            discount_amount=discount_amount,
            shipping_cost=shipping_cost,
            total=total,
            created_at=now,
            updated_at=now,
        )

        return await self._repository.save(
            order,
        )

    async def get_by_id(
        self,
        order_id: int,
        raises: bool = True,
        with_lock: bool = False,
    ) -> Order | None:
        return await self._repository.get_by_id(
            model_id=order_id,
            raises=raises,
            with_lock=with_lock,
        )

    async def get_by_customer_id(
        self,
        customer_id: int,
    ) -> list[Order]:
        return await self._repository.get_by_customer_id(
            customer_id=customer_id,
        )

    async def update_shipping(
        self,
        *,
        order_id: int,
        shipping_cost: Decimal,
    ) -> UpdateOrderShippingResult:

        order = await self._repository.get_by_id(order_id)

        if shipping_cost < Decimal("0.00"):
            raise ValidationError(
                "El coste de envio no puede ser negativo"
            )

        if (
            order.status
            != OrderStatus.PENDING_SHIPPING_QUOTE
        ):
            raise ValidationError(
                "El pedido no esta en espera de cotizacion de envio."
            )

        order.shipping_cost = shipping_cost

        order.total = (
            order.subtotal
            - order.discount_amount
            + shipping_cost
        )

        order.status = (
            OrderStatus.PENDING_PAYMENT
        )

        order = await self._repository.save(
            order,
            flush=True,
        )

        return UpdateOrderShippingResult(
            id=order.id,
            order_number=order.order_number,

            status=order.status,

            shipping_cost=order.shipping_cost,
            total=order.total,
        )