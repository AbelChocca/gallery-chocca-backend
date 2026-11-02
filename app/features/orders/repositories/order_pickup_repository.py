
from sqlalchemy import select

from app.infra.db.repositories.base_repository import BaseRepository

from app.features.orders.entities.order_pickup import OrderPickup
from app.features.orders.models.order_pickup import OrderPickupTable


class OrderPickupRepository(
    BaseRepository[OrderPickup, OrderPickupTable]
):

    async def get_by_order_id(
        self,
        order_id: int,
    ) -> OrderPickup | None:

        statement = select(OrderPickupTable).where(
            OrderPickupTable.order_id == order_id
        )

        result = await self._db_session.execute(statement)
        model = result.scalar_one_or_none()

        return (
            self._base_mapper.to_entity(model)
            if model is not None
            else None
        )
