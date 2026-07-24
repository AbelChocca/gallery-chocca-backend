from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.core.exceptions import ValueNotFound
from app.features.products.variant.product_variant import ProductVariant
from app.infra.db.exceptions import DatabaseException
from app.infra.db.mappers.variant_mapper import VariantMapper
from app.features.products.models.model_product import VariantTable
from app.infra.db.repositories.base_repository import BaseRepository


class VariantRepository(
    BaseRepository[ProductVariant, VariantTable]
):

    async def get_by_id(self, model_id: int) -> ProductVariant:
        stmt = (
            select(VariantTable)
            .options(selectinload(VariantTable.sizes))
            .where(VariantTable.id == model_id)
        )

        result = await self._db_session.execute(stmt)
        variant = result.scalar_one_or_none()

        if variant is None:
            raise ValueNotFound(
                "Variant wasn't found",
                {
                    "event": "get_by_id",
                    "variant_id": model_id,
                },
            )

        return VariantMapper.to_entity(variant)

    async def save(
        self,
        entity: ProductVariant,
    ) -> ProductVariant:
        try:

            if entity.id is None:
                model = VariantMapper.to_db_model(entity)

            else:
                existing = await self._get_model_by_id_non_raise(entity.id)
                model = VariantMapper.to_db_model(
                    entity,
                    existing,
                )

            self._db_session.add(model)
            await self._db_session.flush()

            return await self.get_by_id(model.id)

        except SQLAlchemyError as s:
            raise DatabaseException(
                "Postgres error while saving Variant",
                {
                    "repository": "postgres_variant",
                    "base_model": VariantTable.__name__,
                    "event": "save",
                    "original_error": (
                        s.orig if hasattr(s, "orig") else str(s)
                    ),
                },
            ) from s

    async def _get_model_by_id_non_raise(
        self,
        model_id: int,
    ) -> VariantTable | None:

        stmt = (
            select(VariantTable)
            .options(selectinload(VariantTable.sizes))
            .where(VariantTable.id == model_id)
        )

        result = await self._db_session.execute(stmt)

        return result.scalar_one_or_none()