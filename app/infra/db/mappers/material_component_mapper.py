from app.features.material.entities.material_component import MaterialComponent
from app.infra.db.models.model_material import MaterialComponentTable

class MaterialComponentMapper:

    @staticmethod
    def to_db_model(
        entity: MaterialComponent
    ) -> MaterialComponentTable:
        return MaterialComponentTable(
            id=entity.id,
            material_id=entity.material_id,
            fiber_type=entity.fiber_type,
            percentage=entity.percentage
        )

    @staticmethod
    def to_entity(
        model: MaterialComponentTable
    ) -> MaterialComponent:
        return MaterialComponent(
            id=model.id,
            material_id=model.material_id,
            fiber_type=model.fiber_type,
            percentage=model.percentage
        )