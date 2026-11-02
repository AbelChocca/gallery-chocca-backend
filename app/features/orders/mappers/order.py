from app.infra.db.mappers.base_mapper import BaseMapper

from app.features.orders.entities.order import Order
from app.features.orders.models.order import OrderTable


class OrderMapper(BaseMapper[Order, OrderTable]):

    @staticmethod
    def to_db_model(
        entity: Order,
        existing_model: OrderTable | None = None,
    ) -> OrderTable:
        model = existing_model or OrderTable()

        model.id = entity.id
        model.order_number = entity.order_number
        model.customer_id = entity.customer_id
        model.payment_method = entity.payment_method
        model.status = entity.status

        model.subtotal = entity.subtotal
        model.discount_amount = entity.discount_amount
        model.shipping_cost = entity.shipping_cost
        model.total = entity.total

        model.created_at = entity.created_at
        model.updated_at = entity.updated_at

        return model

    @staticmethod
    def to_entity(model: OrderTable) -> Order:
        return Order(
            id=model.id,
            order_number=model.order_number,
            customer_id=model.customer_id,
            payment_method=model.payment_method,
            status=model.status,
            subtotal=model.subtotal,
            discount_amount=model.discount_amount,
            shipping_cost=model.shipping_cost,
            total=model.total,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )