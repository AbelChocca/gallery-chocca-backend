from app.features.products.variant_size.variant_size import VariantSize
from app.features.products.models.model_product import VariantSizeTable
from app.infra.db.repositories.base_repository import BaseRepository


class VariantSizeRepository(
    BaseRepository[VariantSize, VariantSizeTable]
):
    pass
  