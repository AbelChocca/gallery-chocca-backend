from sqlalchemy import select

from app.core.exceptions import ValueNotFound
from app.features.payments.entities.payment import Payment
from app.features.payments.models.payment import (
    PaymentTable,
)
from app.infra.db.repositories.base_repository import BaseRepository


class PaymentRepository(BaseRepository[Payment, PaymentTable]):

    async def get_by_provider_order_id(
        self,
        provider_order_id: str,
        raises: bool = True,
    ) -> Payment | None:
        stmt = (
            select(PaymentTable)
            .where(
                PaymentTable.provider_order_id
                == provider_order_id
            )
        )

        result = await self._db_session.execute(
            stmt
        )

        model = result.scalar_one_or_none()

        if model is None:
            if raises:
                raise ValueNotFound(
                    "Pago no encontrado.",
                    context={
                        "provider_order_id":
                            provider_order_id,
                    },
                )

            return None

        return self._base_mapper.to_entity(
            model
        )

    async def get_by_provider_payment_id(
        self,
        provider_payment_id: str,
        raises: bool = True,
    ) -> Payment | None:
        statement = select(PaymentTable).where(
            PaymentTable.provider_payment_id == provider_payment_id
        )

        result = await self._db_session.execute(statement)

        model = result.scalar_one_or_none()

        if model is None:
            if raises:
                raise ValueNotFound(
                    f"Payment with provider_payment_id "
                    f"'{provider_payment_id}' not found"
                )

            return None

        return self._base_mapper.to_entity(model)

    async def get_by_order_id(
        self,
        order_id: int,
    ) -> list[Payment]:
        statement = (
            select(PaymentTable)
            .where(PaymentTable.order_id == order_id)
            .order_by(PaymentTable.created_at.desc())
        )

        result = await self._db_session.execute(statement)

        models = result.scalars().all()

        return [
            self._base_mapper.to_entity(model)
            for model in models
        ]