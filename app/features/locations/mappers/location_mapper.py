
from app.features.locations.entities.location import Location
from app.features.locations.models.locations import LocationTable

from app.infra.db.mappers.base_mapper import BaseMapper


class LocationMapper(BaseMapper[Location, LocationTable]):

    @staticmethod
    def to_entity(model: LocationTable) -> Location:
        return Location(
            id=model.id,
            name=model.name,
            type=model.type,
            address=model.address,
            ubigeo_code=model.ubigeo_code,
            latitude=model.latitude,
            longitude=model.longitude,
            phone=model.phone,
            reference=model.reference,
            external_provider=model.external_provider,
            external_code=model.external_code,
            is_active=model.is_active,
            pickup_enabled=model.pickup_enabled,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_db_model(
        entity: Location,
        existing_model: LocationTable | None = None,
    ) -> LocationTable:

        model = existing_model or LocationTable()

        if entity.id is not None:
            model.id = entity.id

        model.name = entity.name
        model.type = entity.type

        model.address = entity.address
        model.ubigeo_code = entity.ubigeo_code

        model.latitude = entity.latitude
        model.longitude = entity.longitude

        model.phone = entity.phone
        model.reference = entity.reference

        model.external_provider = entity.external_provider
        model.external_code = entity.external_code

        model.is_active = entity.is_active
        model.pickup_enabled = entity.pickup_enabled

        if entity.created_at is not None:
            model.created_at = entity.created_at

        if entity.updated_at is not None:
            model.updated_at = entity.updated_at

        return model
