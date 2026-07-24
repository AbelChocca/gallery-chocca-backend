from app.infra.db.repositories.base_repository import BaseRepository
from app.features.products.product import Product
from app.features.products.models.model_product import ProductTable, VariantTable, VariantSizeTable
from app.features.products.variant_size.variant_size import VariantSize
from app.infra.db.mappers.variant_size_mapper import VariantSizeMapper

from app.features.products.product_dto import FilterProductCommand

from app.core.exceptions import ValueNotFound

from typing import List
from sqlmodel.sql.expression import SelectOfScalar, Select
from sqlmodel import select, col, exists, or_
from sqlalchemy.orm import selectinload, noload
from sqlalchemy import func

class PostgresProductRepository(BaseRepository[Product, ProductTable]):
    async def get_variant_size_by_id(
        self,
        variant_size_id: int,
    ) -> VariantSize:

        stmt = (
            select(VariantSizeTable)
            .where(
                VariantSizeTable.id == variant_size_id
            )
        )

        result = await self._db_session.execute(stmt)

        variant_size = result.scalar_one_or_none()

        if variant_size is None:
            raise ValueNotFound(
                "Variant size not found.",
                {
                    "variant_size_id": variant_size_id,
                },
            )

        return VariantSizeMapper.to_entity(variant_size)
    
    def _apply_filters(
        self,
        stmt: Select[ProductTable] | SelectOfScalar[ProductTable],
        filter_command: FilterProductCommand,
    ) -> Select[ProductTable] | SelectOfScalar[ProductTable]:
        if filter_command.name or filter_command.sku:
            conditions = []

            if filter_command.name:
                conditions.append(
                    col(ProductTable.nombre).ilike(f"%{filter_command.name}%")
                )

            if filter_command.sku:
                sku_subquery = (
                    select(1)
                    .select_from(VariantTable)
                    .join(VariantSizeTable, VariantSizeTable.variant_id == VariantTable.id)
                    .where(
                        VariantTable.product_id == ProductTable.id,
                        col(VariantSizeTable.sku).ilike(f"%{filter_command.sku}%")
                    )
                )

                conditions.append(exists(sku_subquery.correlate(ProductTable)))

            stmt = stmt.where(or_(*conditions))

        if filter_command.brand:
            stmt = stmt.where(ProductTable.brand == filter_command.brand)

        if filter_command.category:
            stmt = stmt.where(ProductTable.category == filter_command.category)

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
                )

                if filter_command.sizes:
                    subqr = subqr.where(
                        col(VariantSizeTable.size).in_(filter_command.sizes)
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
        res = (await self._db_session.execute(statement)).scalar_one_or_none()
        if res is None:
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
        filter_dto: FilterProductCommand | None = None
    ) -> int:
        stmt = select(func.count(ProductTable.id))
        if filter_dto is not None:
            stmt = self._apply_filters(stmt, filter_dto)

        result = await self._db_session.execute(stmt)
        return result.scalar() or 0

    async def get_all(
        self,
        filter_command: FilterProductCommand,
        offset: int = 0,
        limit: int = 100,
        load_sizes: bool = False
    ) -> List[Product]:

        variants_loader = selectinload(ProductTable.variants)

        if load_sizes:
            variants_loader = variants_loader.options(
                selectinload(VariantTable.sizes)
            )
        else:
            variants_loader = variants_loader.options(
                noload(VariantTable.sizes)
            )

        stmt = (
            select(ProductTable)
            .options(variants_loader)
        )

        stmt = self._apply_filters(stmt, filter_command)

        stmt = (
            stmt
            .order_by(col(ProductTable.id).desc())
            .offset(offset)
            .limit(limit)
        )

        res = (await self._db_session.execute(stmt)).scalars().all()

        return [
            self._base_mapper.to_entity(product_table)
            for product_table in res
        ]
        
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
    
    async def get_count_by_category(self) -> list[tuple[str, int]]:
        stmt = select(ProductTable.category, func.count()).group_by(ProductTable.category)

        res = await self._db_session.execute(stmt)

        category_counts = res.all()
        if not category_counts: 
            return []
        
        return category_counts
    
    async def get_last_n_products(self, n: int) -> list[Product]:
        stmt = select(ProductTable).order_by(col(ProductTable.id).desc()).limit(n)

        res = await self._db_session.execute(stmt)

        products = res.scalars().all()
        if not products: 
            return []
        
        return [
            self._base_mapper.to_entity(product)
            for product in products
        ]
    