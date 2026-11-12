from app.infra.db.mappers.base_mapper import BaseMapper

from app.features.orders.entities.order_item import OrderItem
from app.features.orders.models.order_item import OrderItemTable
    

class OrderItemMapper(
    BaseMapper[OrderItem, OrderItemTable],
):

    @staticmethod
    def to_db_model(
        entity: OrderItem,
        existing_model: OrderItemTable | None = None,
    ) -> OrderItemTable:
        model = existing_model or OrderItemTable()

        model.id = entity.id
        model.order_id = entity.order_id

        model.product_id = entity.product_id
        model.variant_id = entity.variant_id
        model.variant_size_id = entity.variant_size_id

        model.product_name = entity.product_name
        model.sku = entity.sku
        model.color = entity.color
        model.size = entity.size

        model.quantity = entity.quantity

        model.unit_original_price = entity.unit_original_price
        model.unit_final_price = entity.unit_final_price

        model.original_total = entity.original_total
        model.discount_amount = entity.discount_amount
        model.final_total = entity.final_total

        return model

    @staticmethod
    def to_entity(
        model: OrderItemTable,
    ) -> OrderItem:
        return OrderItem(
            id=model.id,
            order_id=model.order_id,
            product_id=model.product_id,
            variant_id=model.variant_id,
            variant_size_id=model.variant_size_id,
            product_name=model.product_name,
            sku=model.sku,
            color=model.color,
            size=model.size,
            quantity=model.quantity,
            unit_original_price=model.unit_original_price,
            unit_final_price=model.unit_final_price,
            original_total=model.original_total,
            discount_amount=model.discount_amount,
            final_total=model.final_total,
        )