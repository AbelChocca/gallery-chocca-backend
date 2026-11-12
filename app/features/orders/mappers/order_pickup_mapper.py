from app.features.orders.entities.order_pickup import OrderPickup
from app.features.orders.models.order_pickup import OrderPickupTable

from app.infra.db.mappers.base_mapper import BaseMapper

class OrderPickupMapper(BaseMapper[OrderPickup, OrderPickupTable]):

    @staticmethod
    def to_entity(model: OrderPickupTable) -> OrderPickup:
        return OrderPickup(
            id=model.id,
            order_id=model.order_id,
            location_id=model.location_id,
            location_name=model.location_name,
            location_address=model.location_address,
            location_ubigeo_code=model.location_ubigeo_code,
            location_latitude=model.location_latitude,
            location_longitude=model.location_longitude,
            location_phone=model.location_phone,
            location_reference=model.location_reference,
            created_at=model.created_at,
        )

    @staticmethod
    def to_db_model(
        entity: OrderPickup,
        existing_model: OrderPickupTable | None = None,
    ) -> OrderPickupTable:

        model = existing_model or OrderPickupTable()

        model.id = entity.id
        model.order_id = entity.order_id
        model.location_id = entity.location_id
        model.location_name = entity.location_name
        model.location_address = entity.location_address
        model.location_ubigeo_code = entity.location_ubigeo_code
        model.location_latitude = entity.location_latitude
        model.location_longitude = entity.location_longitude
        model.location_phone = entity.location_phone
        model.location_reference = entity.location_reference

        if entity.created_at is not None:
            model.created_at = entity.created_at

        return model
