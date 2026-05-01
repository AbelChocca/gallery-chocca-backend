from app.infra.db.repositories.base_repository import BaseRepository
from app.domain.product.entities.product import Product
from app.domain.product.entities.variant_size import VariantSize
from app.infra.db.models.model_product import ProductTable, VariantTable, VariantSizeTable

from app.domain.product.dto.product_dto import FilterProductCommand

from app.infra.db.exceptions import DatabaseException
from app.core.exceptions import ValueNotFound

from typing import List
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel.sql.expression import SelectOfScalar, Select
from sqlmodel import select, col, exists, or_
from sqlalchemy.orm import selectinload, noload
from sqlalchemy import func

class PostgresProductRepository(BaseRepository[Product, ProductTable]):
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
    
    async def get_inventory_products(
        self,
        filter_command: FilterProductCommand,
        offset: int = 0,
        limit: int = 100,
    ) -> List[Product]:
        stmt = select(ProductTable).options(
                selectinload(ProductTable.variants).options(
                    selectinload(VariantTable.sizes)
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
    
    async def get_count_by_category(self) -> list[tuple[str, int]]:
        stmt = select(ProductTable.categoria, func.count()).group_by(ProductTable.categoria)

        res = await self._db_session.execute(stmt)

        category_counts = res.all()
        return category_counts
    
    async def get_last_n_products(self, n: int) -> list[Product]:
        stmt = select(ProductTable).order_by(col(ProductTable.id).desc()).limit(n)

        res = await self._db_session.execute(stmt)

        products = res.scalars().all()
        return [
            self._base_mapper.to_entity(product)
            for product in products
        ]

    async def save(self, entity: Product) -> Product:
        try:
            if entity.id is None:
                model: ProductTable = self._base_mapper.to_db_model(entity)
            else:
                model: ProductTable = self._base_mapper.to_db_model(entity=entity, existing_model=(await self._get_model_by_id_non_raise(entity.id)))

            self._db_session.add(model)
            await self._db_session.flush()

            return await self.get_by_id(model.id)
        except SQLAlchemyError as s:
            raise DatabaseException(
                "Postgres error while saving",
                {
                    "repository": f"postgres_{Product.__name__.lower()}",
                    "base_model": self._base_model.__name__,
                    "event": "save",
                    "original_error": s.orig if hasattr(s, "orig") else str(s)
                }
                ) from s
        
    async def get_variant_size_by_id(self, variant_size_id: int) -> VariantSize:
        stmt = (
            select(VariantSizeTable)
            .where(VariantSizeTable.id == variant_size_id)
        )

        result = await self._db_session.execute(stmt)

        variant_size = result.scalar_one_or_none()
        if not variant_size:
            raise ValueNotFound(
                "Variant Size wasn't found",
                {
                    "event": "get_variant_size_by_id",
                    "variant_id": variant_size_id
                }
            )
        
        return VariantSize(
            size=variant_size.size,
            stock=variant_size.stock,
            id=variant_size.id,
            sku=variant_size.sku,
            variant_id=variant_size
        )
        
    async def save_variant_size(self, variant_size: VariantSize) -> None:
        try:
            exisiting_variant_size = await self._get_variant_size_table_by_id(variant_size.id, True)
            # Updating attributes
            exisiting_variant_size.stock = variant_size.stock

            self._db_session.add(exisiting_variant_size)
        except SQLAlchemyError as s:
            raise DatabaseException(
                "Postgres error while saving Variant Size",
                {
                    "repository": f"postgres_{Product.__name__.lower()}",
                    "base_model": VariantSizeTable.__name__,
                    "event": "save_variant_size",
                    "original_error": s.orig if hasattr(s, "orig") else str(s)
                }
                ) from s
        
    async def _get_variant_size_table_by_id(self, model_id: int, raise_exception: bool = False) -> VariantSizeTable | None:
        stmt = select(VariantSizeTable).where(VariantSizeTable.id == model_id)
        result = await self._db_session.execute(stmt)

        variant_size = result.scalar_one_or_none()
        if raise_exception and not variant_size:
            raise ValueNotFound(
                "Variant size wasn't found",
                {
                    "event": 'get_variant_size_table_by_id',
                    "variant_size_id": model_id
                }
            )
        
        return variant_size