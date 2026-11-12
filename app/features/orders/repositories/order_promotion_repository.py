from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.infra.db.exceptions import DatabaseException

from app.infra.db.repositories.base_repository import BaseRepository

from app.features.orders.entities.order_promotion import OrderPromotion
from app.features.orders.models.order_promotion import OrderPromotionTable


class OrderPromotionRepository(
    BaseRepository[OrderPromotion, OrderPromotionTable],
):
    async def get_by_order_id(
        self,
        order_id: int,
    ) -> list[OrderPromotion]:
        try:
            statement = (
                select(OrderPromotionTable)
                .where(OrderPromotionTable.order_id == order_id)
                .order_by(OrderPromotionTable.id)
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