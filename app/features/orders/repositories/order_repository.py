from sqlalchemy import select, or_, func
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from app.infra.db.exceptions import DatabaseException
from app.features.orders.types.order import OrderFilters, AdminOrderListItemDTO, OrderStatus
from app.infra.db.repositories.base_repository import BaseRepository
from app.features.customer.models.customer import Customer

from app.features.orders.entities.order import Order

from app.features.orders.models.order import (
    OrderTable,
    order_number_sequence,
)


class OrderRepository(BaseRepository[Order, OrderTable]):

    async def get_expired_pending_orders(
        self,
        *,
        expired_before: datetime,
        with_lock: bool = False,
    ) -> list[Order]:
        statement = select(
        OrderTable
        ).where(
            OrderTable.status
            == OrderStatus.PENDING_PAYMENT,

            OrderTable.created_at
            <= expired_before,
        )

        if with_lock:
            statement = statement.with_for_update()

        result = await self._db_session.execute(
            statement
        )

        models = result.scalars().all()

        return [
            self._base_mapper.to_entity(model)
            for model in models
        ]

    async def get_admin_orders(
        self,
        *,
        filters: OrderFilters,
        offset: int,
        limit: int,
    ) -> tuple[
        list[AdminOrderListItemDTO],
        int,
    ]:
        conditions = []

        if filters.status is not None:
            conditions.append(
                OrderTable.status == filters.status
            )

        if filters.created_at_from is not None:
            conditions.append(
                OrderTable.created_at >= filters.created_at_from
            )

        if filters.created_at_to is not None:
            conditions.append(
                OrderTable.created_at <= filters.created_at_to
            )

        if filters.search:
            search = filters.search.strip()

            search_pattern = f"%{search}%"

            conditions.append(
                or_(
                    OrderTable.order_number.ilike(
                        search_pattern
                    ),
                    Customer.name.ilike(
                        search_pattern
                    ),
                    Customer.last_name.ilike(
                        search_pattern
                    ),
                    func.concat(
                        Customer.name,
                        " ",
                        Customer.last_name,
                    ).ilike(search_pattern),
                )
            )

        base_query = (
            select(
                OrderTable.id,
                OrderTable.order_number,
                OrderTable.customer_id,

                Customer.name,
                Customer.last_name,

                OrderTable.status,
                OrderTable.subtotal,
                OrderTable.discount_amount,
                OrderTable.shipping_cost,
                OrderTable.total,
                OrderTable.created_at,
            )
            .join(
                Customer,
                Customer.id == OrderTable.customer_id,
            )
            .where(*conditions)
        )

        count_query = (
            select(
                func.count(OrderTable.id)
            )
            .join(
                Customer,
                Customer.id == OrderTable.customer_id,
            )
            .where(*conditions)
        )

        total_items = (
            await self._db_session.scalar(
                count_query
            )
        ) or 0

        result = await self._db_session.execute(
            base_query
            .order_by(
                OrderTable.created_at.desc()
            )
            .offset(offset)
            .limit(limit)
        )

        rows = result.all()

        items = [
            AdminOrderListItemDTO(
                id=row.id,
                order_number=row.order_number,

                customer_id=row.customer_id,

                customer_name=(
                    f"{row.name} {row.last_name}"
                ).strip(),

                status=row.status,

                subtotal=row.subtotal,
                discount_amount=row.discount_amount,
                shipping_cost=row.shipping_cost,
                total=row.total,

                created_at=row.created_at,
            )
            for row in rows
        ]

        return items, total_items

    async def get_by_customer_id(
        self,
        customer_id: int,
    ) -> list[Order]:
        try:
            statement = (
                select(OrderTable)
                .where(OrderTable.customer_id == customer_id)
                .order_by(OrderTable.created_at.desc())
            )

            result = await self._db_session.execute(statement)

            models = result.scalars().all()

            return [
                self._base_mapper.to_entity(model)
                for model in models
            ]

        except SQLAlchemyError as exc:
            raise DatabaseException(
                "Postgres error while getting customer orders.",
                {
                    "repository": "postgres_order",
                    "event": "get_by_customer_id",
                    "customer_id": customer_id,
                },
            ) from exc

    async def next_order_sequence(self) -> int:
        try:
            result = await self._db_session.execute(
                select(order_number_sequence.next_value())
            )

            return result.scalar_one()

        except SQLAlchemyError as exc:
            raise DatabaseException(
                "Postgres error while generating order sequence.",
                {
                    "repository": "postgres_order",
                    "base_model": OrderTable.__name__,
                    "event": "next_order_sequence",
                    "original_error": str(getattr(exc, "orig", exc)),
                },
            ) from exc