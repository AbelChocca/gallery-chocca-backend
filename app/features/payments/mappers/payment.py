from app.features.payments.entities.payment import (
    Payment,
)
from app.features.payments.models.payment import (
    PaymentTable,
)
from app.infra.db.mappers.base_mapper import (
    BaseMapper,
)


class PaymentMapper(
    BaseMapper[
        Payment,
        PaymentTable,
    ]
):

    @staticmethod
    def to_db_model(
        entity: Payment,
        existing_model: PaymentTable | None = None,
    ) -> PaymentTable:
        if existing_model is None:
            return PaymentTable(
                id=entity.id,
                order_id=entity.order_id,
                provider=entity.provider,
                status=entity.status,
                amount=entity.amount,
                payment_method=entity.payment_method,
                currency=entity.currency,

                provider_payment_id=(
                    entity.provider_payment_id
                ),
                provider_order_id=(
                    entity.provider_order_id
                ),

                checkout_id=entity.checkout_id,
                payment_link=entity.payment_link,
                expires_at=entity.expires_at,

                authorization=entity.authorization,

                error_code=entity.error_code,
                error_message=entity.error_message,

                created_at=entity.created_at,
                updated_at=entity.updated_at,
            )

        existing_model.order_id = (
            entity.order_id
        )
        existing_model.provider = (
            entity.provider
        )
        existing_model.payment_method = entity.payment_method
        existing_model.status = (
            entity.status
        )
        existing_model.amount = (
            entity.amount
        )
        existing_model.currency = (
            entity.currency
        )

        existing_model.provider_payment_id = (
            entity.provider_payment_id
        )
        existing_model.provider_order_id = (
            entity.provider_order_id
        )

        existing_model.checkout_id = (
            entity.checkout_id
        )
        existing_model.payment_link = (
            entity.payment_link
        )
        existing_model.expires_at = (
            entity.expires_at
        )

        existing_model.authorization = (
            entity.authorization
        )

        existing_model.error_code = (
            entity.error_code
        )
        existing_model.error_message = (
            entity.error_message
        )

        existing_model.created_at = (
            entity.created_at
        )
        existing_model.updated_at = (
            entity.updated_at
        )

        return existing_model

    @staticmethod
    def to_entity(
        model: PaymentTable,
    ) -> Payment:
        return Payment(
            id=model.id,

            order_id=model.order_id,

            provider=model.provider,
            payment_method=model.payment_method,
            status=model.status,

            amount=model.amount,
            currency=model.currency,

            provider_payment_id=(
                model.provider_payment_id
            ),
            provider_order_id=(
                model.provider_order_id
            ),

            checkout_id=model.checkout_id,
            payment_link=model.payment_link,
            expires_at=model.expires_at,

            authorization=model.authorization,

            error_code=model.error_code,
            error_message=model.error_message,

            created_at=model.created_at,
            updated_at=model.updated_at,
        )