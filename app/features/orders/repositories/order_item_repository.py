from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.infra.db.exceptions import DatabaseException

from app.infra.db.repositories.base_repository import BaseRepository

from app.features.orders.entities.order_item import OrderItem
from app.features.orders.models.order_item import OrderItemTable


class OrderItemRepository(
    BaseRepository[OrderItem, OrderItemTable],
):
    async def get_by_order_ids(
        self,
        order_ids: list[int],
    ) -> list[OrderItem]:
        if not order_ids:
            return []

        stmt = (
            select(OrderItemTable)
            .where(
                OrderItemTable.order_id.in_(
                    order_ids,
                )
            )
            .order_by(
                OrderItemTable.order_id,
                OrderItemTable.id,
            )
        )

        result = await self._db_session.execute(
            stmt
        )

        return [
            self._base_mapper.to_entity(model)
            for model in result.scalars().all()
        ]
    
    async def get_by_order_id(
        self,
        order_id: int,
    ) -> list[OrderItem]:
        try:
            statement = (
                select(OrderItemTable)
                .where(OrderItemTable.order_id == order_id)
                .order_by(OrderItemTable.id)
            )

            result = await self._db_session.execute(statement)

            models = result.scalars().all()

            return [
                self._base_mapper.to_entity(model)
                for model in models
            ]

        except SQLAlchemyError as exc:
            raise DatabaseException(
                "Postgres error while getting order items.",
                {
                    "repository": "postgres_order_item",
                    "event": "get_by_order_id",
                    "order_id": order_id,
                },
            ) from exc