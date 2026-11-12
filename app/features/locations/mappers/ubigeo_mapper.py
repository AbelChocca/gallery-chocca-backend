from app.infra.db.mappers.base_mapper import BaseMapper

from app.features.locations.entities.ubigeo import Ubigeo
from app.features.locations.models.ubigeo import UbigeoTable


class UbigeoMapper(
    BaseMapper[Ubigeo, UbigeoTable],
):

    @staticmethod
    def to_db_model(
        entity: Ubigeo,
        existing_model: UbigeoTable | None = None,
    ) -> UbigeoTable:
        model = existing_model or UbigeoTable()

        model.code = entity.code
        model.department = entity.department
        model.province = entity.province
        model.district = entity.district
        model.city_name = entity.city_name

        return model

    @staticmethod
    def to_entity(
        model: UbigeoTable,
    ) -> Ubigeo:
        return Ubigeo(
            code=model.code,
            department=model.department,
            province=model.province,
            district=model.district,
            city_name=model.city_name,
        )