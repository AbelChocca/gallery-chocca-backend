from typing import Optional

from app.features.material.entity import Material

from app.infra.db.mappers.base_mapper import BaseMapper
from app.infra.db.models.model_material import MaterialTable


class MaterialMapper(
    BaseMapper[Material, MaterialTable]
):

    @staticmethod
    def to_db_model(
        entity: Material,
        existing_model: Optional[MaterialTable] = None
    ) -> MaterialTable:

        if existing_model is None:
            return MaterialTable(
                id=entity.id,
                code=entity.code,
                name=entity.name,
                description=entity.description,
                company=entity.company,
                material_type=entity.material_type,
                stock=entity.stock,
                minimum_stock=entity.minimum_stock,
                unit_type=entity.unit_type,
                is_active=entity.is_active,
                created_at=entity.created_at,
                updated_at=entity.updated_at
            )

        existing_model.code = entity.code
        existing_model.name = entity.name
        existing_model.description = entity.description
        existing_model.company = entity.company
        existing_model.stock = entity.stock
        existing_model.minimum_stock = entity.minimum_stock
        existing_model.material_type = entity.material_type
        existing_model.unit_type = entity.unit_type
        existing_model.is_active = entity.is_active
        existing_model.updated_at = entity.updated_at

        return existing_model

    @staticmethod
    def to_entity(
        model: MaterialTable
    ) -> Material:
        return Material(
            id=model.id,
            code=model.code,
            name=model.name,
            description=model.description,
            company=model.company,
            stock=model.stock,
            minimum_stock=model.minimum_stock,
            material_type=model.material_type,
            unit_type=model.unit_type,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )