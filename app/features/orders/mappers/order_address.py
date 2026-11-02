from app.infra.db.mappers.base_mapper import BaseMapper

from app.features.orders.entities.order_address import OrderAddress
from app.features.orders.models.order_address import OrderAddressTable


class OrderAddressMapper(
    BaseMapper[OrderAddress, OrderAddressTable],
):

    @staticmethod
    def to_db_model(
        entity: OrderAddress,
        existing_model: OrderAddressTable | None = None,
    ) -> OrderAddressTable:
        model = existing_model or OrderAddressTable()

        model.id = entity.id
        model.order_id = entity.order_id

        model.recipient_name = entity.recipient_name
        model.phone = entity.phone

        model.ubigeo_code = entity.ubigeo_code
        model.address = entity.address

        model.latitude = entity.latitude
        model.longitude = entity.longitude

        model.reference = entity.reference
        model.delivery_instructions = entity.delivery_instructions

        return model

    @staticmethod
    def to_entity(
        model: OrderAddressTable,
    ) -> OrderAddress:
        return OrderAddress(
            id=model.id,
            order_id=model.order_id,
            recipient_name=model.recipient_name,
            phone=model.phone,
            ubigeo_code=model.ubigeo_code,
            address=model.address,
            latitude=model.latitude,
            longitude=model.longitude,
            reference=model.reference,
            delivery_instructions=model.delivery_instructions,
        )