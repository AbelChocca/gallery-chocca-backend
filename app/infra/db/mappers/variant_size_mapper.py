from app.features.products.variant_size.variant_size import VariantSize

from app.infra.db.mappers.base_mapper import BaseMapper
from app.features.products.models.model_product import VariantSizeTable


class VariantSizeMapper(BaseMapper[VariantSize, VariantSizeTable]):

    @staticmethod
    def to_entity(model: VariantSizeTable) -> VariantSize:
        return VariantSize(
            id=model.id,
            variant_id=model.variant_id,
            size=model.size,
            barcode=model.barcode,
            sku=model.sku,
        )

    @staticmethod
    def to_db_model(
        entity: VariantSize,
        existing_model: VariantSizeTable | None = None,
    ) -> VariantSizeTable:

        if existing_model:
            existing_model.size = entity.size
            existing_model.barcode = entity.barcode
            existing_model.sku = entity.sku
            return existing_model

        return VariantSizeTable(
            size=entity.size,
            barcode=entity.barcode,
            sku=entity.sku,
        )