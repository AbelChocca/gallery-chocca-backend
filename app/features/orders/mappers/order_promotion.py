from app.infra.db.mappers.base_mapper import BaseMapper

from app.features.orders.entities.order_promotion import OrderPromotion
from app.features.orders.models.order_promotion import OrderPromotionTable


class OrderPromotionMapper(
    BaseMapper[OrderPromotion, OrderPromotionTable],
):

    @staticmethod
    def to_db_model(
        entity: OrderPromotion,
        existing_model: OrderPromotionTable | None = None,
    ) -> OrderPromotionTable:
        model = existing_model or OrderPromotionTable()

        model.id = entity.id
        model.order_id = entity.order_id

        model.promotion_id = entity.promotion_id

        model.name = entity.name
        model.application_scope = entity.application_scope

        model.coupon_code = entity.coupon_code

        model.discount_amount = entity.discount_amount

        return model

    @staticmethod
    def to_entity(
        model: OrderPromotionTable,
    ) -> OrderPromotion:
        return OrderPromotion(
            id=model.id,
            order_id=model.order_id,
            promotion_id=model.promotion_id,
            name=model.name,
            application_scope=model.application_scope,
            coupon_code=model.coupon_code,
            discount_amount=model.discount_amount,
        )