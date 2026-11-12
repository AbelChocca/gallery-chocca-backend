from app.infra.db.mappers.base_mapper import BaseMapper

from app.features.orders.entities.order_billing import OrderBilling
from app.features.orders.models.order_billing import OrderBillingTable


class OrderBillingMapper(
    BaseMapper[OrderBilling, OrderBillingTable],
):

    @staticmethod
    def to_db_model(
        entity: OrderBilling,
        existing_model: OrderBillingTable | None = None,
    ) -> OrderBillingTable:
        model = existing_model or OrderBillingTable()

        model.id = entity.id
        model.order_id = entity.order_id

        model.document_type = entity.document_type

        model.identity_document_type = (
            entity.identity_document_type
        )

        model.identity_document_number = (
            entity.identity_document_number
        )

        model.recipient_name = entity.recipient_name

        model.email = entity.email
        model.billing_address = entity.billing_address

        return model

    @staticmethod
    def to_entity(
        model: OrderBillingTable,
    ) -> OrderBilling:
        return OrderBilling(
            id=model.id,
            order_id=model.order_id,
            document_type=model.document_type,
            identity_document_type=model.identity_document_type,
            identity_document_number=model.identity_document_number,
            recipient_name=model.recipient_name,
            email=model.email,
            billing_address=model.billing_address,
        )