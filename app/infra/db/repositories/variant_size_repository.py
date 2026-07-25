from app.features.products.variant_size.variant_size import VariantSize
from app.features.products.models.model_product import VariantSizeTable
from app.infra.db.repositories.base_repository import BaseRepository

from sqlalchemy import select


class VariantSizeRepository(
    BaseRepository[VariantSize, VariantSizeTable]
):
    async def get_all(
        self,
        *,
        limit: int = 100,
        offset: int = 0,
    ) -> list[VariantSize]:

        statement = (
            select(VariantSizeTable)
            .offset(offset)
            .limit(limit)
        )

        result = await self._db_session.execute(statement)

        variant_sizes = result.all()

        return [
            self._base_mapper.to_entity(item)
            for item in variant_sizes
        ]
  