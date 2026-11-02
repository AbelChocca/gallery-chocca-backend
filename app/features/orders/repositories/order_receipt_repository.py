from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.infra.db.exceptions import (
    DatabaseException,
)
from app.core.exceptions import (
    ValueNotFound,
)

from app.infra.db.repositories.base_repository import (
    BaseRepository,
)

from app.features.orders.entities.order_receipt import (
    OrderReceipt,
)
from app.features.orders.models.order_receipt import (
    OrderReceiptTable,
)


class OrderReceiptRepository(
    BaseRepository[
        OrderReceipt,
        OrderReceiptTable,
    ],
):

    async def get_by_order_id(
        self,
        *,
        order_id: int,
        raises: bool = True,
        with_lock: bool = False,
    ) -> OrderReceipt | None:
        try:
            statement = (
                select(OrderReceiptTable)
                .where(
                    OrderReceiptTable.order_id
                    == order_id
                )
            )

            if with_lock:
                statement = (
                    statement.with_for_update()
                )

            result = await (
                self._db_session.execute(
                    statement
                )
            )

            model = (
                result.scalar_one_or_none()
            )

            if model is None:
                if not raises:
                    return None

                raise ValueNotFound(
                    message=(
                        "Order receipt wasn't found."
                    ),
                    context={
                        "repository":
                            "postgres_order_receipt",
                        "event":
                            "get_by_order_id",
                        "order_id":
                            order_id,
                    },
                )

            return self._base_mapper.to_entity(
                model
            )

        except SQLAlchemyError as exc:
            raise DatabaseException(
                message=(
                    "Postgres error while getting "
                    "order receipt."
                ),
                context={
                    "repository":
                        "postgres_order_receipt",
                    "event":
                        "get_by_order_id",
                    "order_id":
                        order_id,
                },
            ) from exc