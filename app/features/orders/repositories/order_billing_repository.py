from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.infra.db.exceptions import DatabaseException
from app.core.exceptions import ValueNotFound

from app.infra.db.repositories.base_repository import BaseRepository

from app.features.orders.entities.order_billing import OrderBilling
from app.features.orders.models.order_billing import OrderBillingTable


class OrderBillingRepository(
    BaseRepository[OrderBilling, OrderBillingTable],
):
    async def get_by_order_id(
        self,
        order_id: int,
        raises: bool = True,
    ) -> OrderBilling | None:
        try:
            statement = select(OrderBillingTable).where(
                OrderBillingTable.order_id == order_id
            )

            result = await self._db_session.execute(statement)

            model = result.scalar_one_or_none()

            if model is None:
                if not raises:
                    return None

                raise ValueNotFound(
                    "Order address wasn't found.",
                    {
                        "repository": "postgres_order_address",
                        "event": "get_by_order_id",
                        "order_id": order_id,
                    },
                )

            return self._base_mapper.to_entity(model)

        except SQLAlchemyError as exc:
            raise DatabaseException(
                "Postgres error while getting order address.",
                {
                    "repository": "postgres_order_address",
                    "event": "get_by_order_id",
                    "order_id": order_id,
                },
            ) from exc