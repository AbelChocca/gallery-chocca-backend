from typing import Optional

from app.features.material.entities.material import Material

from app.infra.db.mappers.base_mapper import BaseMapper
from app.features.material.models.model_material import MaterialTable
from app.infra.db.mappers.material_component_mapper import MaterialComponentMapper


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
                minimum_stock=entity.minimum_stock,
                stock=entity.stock,
                company=entity.company,
                material_type=entity.material_type,
                unit_type=entity.unit_type,
                is_active=entity.is_active,
                created_at=entity.created_at,
                updated_at=entity.updated_at,
                components=[
                    MaterialComponentMapper.to_db_model(component)
                    for component in entity.components
                ]
            )

        existing_model.code = entity.code
        existing_model.name = entity.name
        existing_model.stock = entity.stock
        existing_model.minimum_stock = entity.minimum_stock
        existing_model.description = entity.description
        existing_model.company = entity.company
        existing_model.material_type = entity.material_type
        existing_model.unit_type = entity.unit_type
        existing_model.is_active = entity.is_active
        existing_model.updated_at = entity.updated_at
        existing_model.components = [
            MaterialComponentMapper.to_db_model(component)
            for component in entity.components
        ]

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
            minimum_stock=model.minimum_stock,
            stock=model.stock,
            company=model.company,
            material_type=model.material_type,
            unit_type=model.unit_type,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
             components=[
                MaterialComponentMapper.to_entity(component)
                for component in model.components
            ]
        )