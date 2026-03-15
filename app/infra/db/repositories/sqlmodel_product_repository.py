from app.infra.db.repositories.base_repository import BaseRepository
from app.domain.product.entities.product import Product
from app.infra.db.models.model_product import ProductTable, VariantTable, VariantSizeTable

from app.domain.product.dto.product_dto import FilterProductCommand

from app.infra.db.exceptions import DatabaseException
from app.core.exceptions import ValueNotFound

from typing import List
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel.sql.expression import SelectOfScalar, Select
from sqlmodel import select, col, exists, delete
from sqlalchemy.orm import selectinload, noload
from sqlalchemy import func

class PostgresProductRepository(BaseRepository[Product, ProductTable]):
    def _apply_filters(
        self,
        stmt: Select[ProductTable] | SelectOfScalar[ProductTable],
        filter_command: FilterProductCommand,
    ) -> Select[ProductTable] | SelectOfScalar[ProductTable]:

        if filter_command.name:
            stmt = stmt.where(col(ProductTable.nombre).ilike(f"%{filter_command.name}%"))

        if filter_command.marca:
            stmt = stmt.where(ProductTable.marca == filter_command.marca)

        if filter_command.categoria:
            stmt = stmt.where(ProductTable.categoria == filter_command.categoria)

        if filter_command.model_family:
            stmt = stmt.where(ProductTable.model_family == filter_command.model_family)

        if filter_command.colors or filter_command.sizes:
            subqr = (
                select(1)
                .select_from(VariantTable)
                .where(VariantTable.product_id == ProductTable.id)
            )

            if filter_command.colors:
                subqr = subqr.where(col(VariantTable.color).in_(filter_command.colors))

            if filter_command.sizes:
                subqr = (
                    subqr
                    .join(VariantSizeTable, VariantSizeTable.variant_id == VariantTable.id)
                    .where(col(VariantSizeTable.size).in_(filter_command.sizes))
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
        res = (await self._db_session.execute(statement)).scalar()
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
        filter_dto: FilterProductCommand
    ) -> int:
        stmt = select(func.count(ProductTable.id))
        stmt = self._apply_filters(stmt, filter_dto)

        result = await self._db_session.execute(stmt)
        return result.scalar() or 0

    async def get_all(
        self,
        filter_command: FilterProductCommand,
        offset: int = 0,
        limit: int = 100,
    ) -> List[Product]:
        stmt = select(ProductTable).options(
                selectinload(ProductTable.variants).options(
                    noload(VariantTable.sizes)
                )
            )
        stmt = self._apply_filters(stmt, filter_command)
            
        
        stmt = (
            stmt
            .order_by(col(ProductTable.id).desc())
            .offset(offset)
            .limit(limit)
        )

        res = (await self._db_session.execute(stmt)).scalars().all()

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

        products = (await self._db_session.execute(statement)).scalars().all()
        return [
            self._base_mapper.to_entity(product)
            for product in products
        ]
        
    async def delete_sizes_batch(self, size_ids: list[int]) -> None:
        try:
            statement = (
                delete(VariantSizeTable)
                .where(col(VariantSizeTable.id).in_(size_ids))
            )
            await self._db_session.execute(statement)
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Cannot delete sizes in database",
                {
                    "size_ids": size_ids,
                    "event": "delete_size_by_id"
                }
                ) from e
        
    async def delete_variants_batch(self, variants_ids: list[int]) -> None:
        if not variants_ids: return None
        try:
            statement = (
                delete(VariantTable)
                .where(col(VariantTable.id).in_(variants_ids))
            )
            await self._db_session.execute(statement)
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Cannot delete variants in database",
                {
                    "variant_ids": variants_ids,
                    "event": "delete_variants_batch"
                }
                ) from e