from app.infra.db.repositories.base_repository import BaseRepository
from app.domain.product.entities.product import Product
from app.infra.db.models.model_product import ProductTable, VariantTable, VariantSizeTable

from app.domain.product.dto.product_dto import FilterSchemaDTO

from app.infra.db.exceptions import DatabaseException
from app.core.exceptions import ValueNotFound

from typing import List
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel.sql.expression import SelectOfScalar, Select
from sqlmodel import select, col, exists
from sqlalchemy.orm import selectinload, noload
from sqlalchemy import func

class PostgresProductRepository(BaseRepository[Product, ProductTable]):
    def _apply_filters(
        self,
        stmt: Select[ProductTable] | SelectOfScalar[ProductTable],
        filter_dto: FilterSchemaDTO,
    ) -> Select[ProductTable] | SelectOfScalar[ProductTable]:

        if filter_dto.name:
            stmt = stmt.where(ProductTable.nombre.ilike(f"%{filter_dto.name}%"))

        if filter_dto.marca:
            stmt = stmt.where(ProductTable.marca == filter_dto.marca)

        if filter_dto.categoria:
            stmt = stmt.where(ProductTable.categoria == filter_dto.categoria)

        if filter_dto.model_family:
            stmt = stmt.where(ProductTable.model_family == filter_dto.model_family)

        if filter_dto.colors or filter_dto.sizes:
            subqr = (
                select(1)
                .select_from(VariantTable)
                .where(VariantTable.product_id == ProductTable.id)
            )

            if filter_dto.colors:
                subqr = subqr.where(col(VariantTable.color).in_(filter_dto.colors))

            if filter_dto.sizes:
                subqr = (
                    subqr
                    .join(VariantSizeTable, VariantSizeTable.variant_id == VariantTable.id)
                    .where(col(VariantSizeTable.size).in_(filter_dto.sizes))
                )

            stmt = stmt.where(exists(subqr.correlate(ProductTable)))

        return stmt

    async def get_by_id(self, model_id: int) -> Product:
        statement = (
            select(ProductTable)
            .options(
                selectinload(ProductTable.variants)
                .selectinload(VariantTable.sizes)
                )
            .where(ProductTable.id == model_id)
        )
        res = (await self._db_session.exec(statement)).first()
        if not res:
            raise ValueNotFound(
                "Product wasn't found",
                { 
                    "product_id": model_id,
                    "event": "get_by_id",
                    "repository": "postgres_product"
                }
                )
        return self._base_mapper.to_entity(res)

    async def count_filtered_products(
        self,
        filter_dto: FilterSchemaDTO
    ) -> int:
        stmt = select(func.count(ProductTable.id))
        stmt = self._apply_filters(stmt, filter_dto)

        result = await self._db_session.exec(stmt)
        return result.one() or 0

    async def get_all(
        self,
        filter_dto: FilterSchemaDTO,
        offset: int = 0,
        limit: int = 100,
    ) -> List[Product]:
        stmt = select(ProductTable).options(
                selectinload(ProductTable.variants).options(
                    noload(VariantTable.sizes)
                )
            )
        stmt = self._apply_filters(stmt, filter_dto)
            
        
        stmt = (
            stmt
            .order_by(col(ProductTable.id).desc())
            .offset(offset)
            .limit(limit)
        )

        res = (await self._db_session.exec(stmt)).all()

        products = [
            self._base_mapper.to_entity(product_table)
            for product_table in res
        ]
        return products
        
    async def search_related(self, query: str, offset: int, limit: int) -> List[Product]:
        statement = (
            select(ProductTable)
            .options(selectinload(ProductTable.variants))
            .where(col(ProductTable.nombre).ilike((f"%{query}%")))
            .offset(offset)
            .limit(limit)
        )

        products = (await self._db_session.exec(statement)).all()
        return [
            self._base_mapper.to_entity(product)
            for product in products
        ]
        
    async def delete_variant_by_id(self, variant_id: int | None = None) -> None:
        if not variant_id: return None
        try:
            statement = (
                select(VariantTable)
                .where(VariantTable.id == variant_id)
            )
            variant = (await self._db_session.exec(statement)).first()
            if not variant:
                return None
            await self._db_session.delete(variant)
            await self._db_session.commit()
        except SQLAlchemyError as e:
            await self._db_session.rollback()
            raise DatabaseException(
                "Cannot delete the variant in database",
                {
                    "variant_id": variant_id,
                    "event": "delete_variant_by_id"
                }
                ) from e
        
    async def delete_size_by_id(self, size_id: int) -> None:
        try:
            statement = (
                select(VariantSizeTable)
                .where(VariantSizeTable.id == size_id)
            )
            variant_size = (await self._db_session.exec(statement)).first()
            if not variant_size:
                return None
            await self._db_session.delete(variant_size)
            await self._db_session.commit()
        except SQLAlchemyError as e:
            await self._db_session.rollback()
            raise DatabaseException(
                "Cannot delete the in database",
                {
                    "size_id": size_id,
                    "event": "delete_size_by_id"
                }
                ) from e