from app.infra.db.mappers.base_mapper import BaseMapper

from app.features.orders.entities.order_receipt import (
    OrderReceipt,
)
from app.features.orders.models.order_receipt import (
    OrderReceiptTable,
)


class OrderReceiptMapper(
    BaseMapper[OrderReceipt, OrderReceiptTable],
):

    @staticmethod
    def to_db_model(
        entity: OrderReceipt,
        existing_model: OrderReceiptTable | None = None,
    ) -> OrderReceiptTable:
        model = existing_model or OrderReceiptTable()

        model.id = entity.id
        model.order_id = entity.order_id

        model.status = entity.status

        model.external_id = entity.external_id
        model.series_number = entity.series_number

        model.provider_error_code = (
            entity.provider_error_code
        )
        model.provider_error_message = (
            entity.provider_error_message
        )

        model.issued_at = entity.issued_at

        model.email_provider_id = (
            entity.email_provider_id
        )
        model.email_sent_at = (
            entity.email_sent_at
        )
        model.email_error_message = (
            entity.email_error_message
        )

        model.created_at = entity.created_at
        model.updated_at = entity.updated_at

        return model

    @staticmethod
    def to_entity(
        model: OrderReceiptTable,
    ) -> OrderReceipt:
        return OrderReceipt(
            id=model.id,
            order_id=model.order_id,

            status=model.status,

            external_id=model.external_id,
            series_number=model.series_number,

            provider_error_code=(
                model.provider_error_code
            ),
            provider_error_message=(
                model.provider_error_message
            ),

            issued_at=model.issued_at,

            email_provider_id=(
                model.email_provider_id
            ),
            email_sent_at=model.email_sent_at,
            email_error_message=(
                model.email_error_message
            ),

            created_at=model.created_at,
            updated_at=model.updated_at,
        )