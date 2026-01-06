from app.infra.db.repositories.base_repository import BaseRepository
from app.modules.product.domain.entities.product import Product
from app.infra.db.models.product_model import ProductTable, VariantColorTable, VariantImageTable
from app.infra.db.mappers.product_mapper import ProductMapper

from app.modules.product.domain.dto.product_dto import FilterSchemaDTO

from app.infra.db.exceptions import DatabaseException

from typing import List
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func

class PostgresProductRepository(BaseRepository[Product, ProductTable]):
    async def count_filtered_products(
        self,
        filter_dto: FilterSchemaDTO
    ) -> int:
        stmt = select(func.count(ProductTable.id))

        if filter_dto.name is not None:
            stmt = stmt.where(ProductTable.nombre.ilike(f"%{filter_dto.name}%"))

        if filter_dto.marca is not None:
            stmt = stmt.where(ProductTable.marca == filter_dto.marca)

        if filter_dto.categoria is not None:
            stmt = stmt.where(ProductTable.categoria == filter_dto.categoria)

        if filter_dto.modelo is not None:
            stmt = stmt.where(ProductTable.modelo == filter_dto.modelo)

        if filter_dto.minPrice is not None:
            stmt = stmt.where(ProductTable.precio >= filter_dto.minPrice)

        if filter_dto.maxPrice is not None:
            stmt = stmt.where(ProductTable.precio <= filter_dto.maxPrice)

        if filter_dto.promocion is not None:
            stmt = stmt.where(ProductTable.promocion == filter_dto.promocion)

        if filter_dto.color is not None:
            stmt = (
                stmt.join(ProductTable.variants)
                .where(VariantColorTable.color == filter_dto.color)
                .distinct()
            )
        result = await self._db_session.exec(stmt)
        row = result.first()
        return row if row else 0

    async def get_all(
        self,
        filter_dto: FilterSchemaDTO,
        offset: int = 0,
        limit: int = 100,
    ) -> List[Product]:
        stmt = (
            select(ProductTable)
            .options(selectinload(ProductTable.variants))) # Definimos consulta estandar

        if filter_dto.name is not None:
            stmt = stmt.where(ProductTable.nombre.ilike(f"%{filter_dto.name}%"))

        if filter_dto.marca is not None:
            stmt = stmt.where(ProductTable.marca == filter_dto.marca)

        if filter_dto.categoria is not None:
            stmt = stmt.where(ProductTable.categoria == filter_dto.categoria)

        if filter_dto.modelo is not None:
            stmt = stmt.where(ProductTable.modelo == filter_dto.modelo)

        if filter_dto.minPrice is not None:
            stmt = stmt.where(ProductTable.precio >= filter_dto.minPrice)

        if filter_dto.maxPrice is not None:
            stmt = stmt.where(ProductTable.precio <= filter_dto.maxPrice)

        if filter_dto.promocion is not None:
            stmt = stmt.where(ProductTable.promocion == filter_dto.promocion)

        if filter_dto.color is not None:
            stmt = (
                stmt.join(ProductTable.variants)
                .where(VariantColorTable.color == filter_dto.color)
                .distinct()
            )
            
        stmt = stmt.offset(offset).limit(limit)

        res = (await self._db_session.exec(stmt)).all()

        products = [
            ProductMapper.to_entity(product_table)
            for product_table in res
        ]
        return products
        
    async def search_related(self, query: str, offset: int, limit: int) -> List[Product]:
        try:
            statement = (
                select(ProductTable)
                .options(selectinload(ProductTable.variants))
                .where(ProductTable.nombre.ilike((f"%{query}%")))
                .offset(offset)
                .limit(limit)
            )

            products = await self._db_session.exec(statement)
            return [
                ProductMapper.to_entity(product)
                for product in products
            ]
        except SQLAlchemyError as s:
            self._logger.error(f"SQLModel error for get products related to {query}: {str(s)}")
            raise DatabaseException(f"Cannot get the related products of {query}") from s
        
    async def delete_variant_by_id(self, variant_id: int) -> None:
        try:
            variant = await self._db_session.get(VariantColorTable, variant_id)
            if not variant:
                self._logger.error(f"Variant with id: {variant_id} was not found in database, delete option cancelled.")
                return None

            await self._db_session.delete(variant)
            await self._db_session.commit()
            self._logger.info(f"Variant with id: {variant_id} was deleted successfuly from database")
        except SQLAlchemyError as e:
            await self._db_session.rollback()
            raise DatabaseException(f"Cannot delete the variant with id: {variant_id} from database") from e

    async def delete_image_by_id(self, image_id: str) -> None:
        try:
            statement = select(VariantImageTable).where(VariantImageTable.cloudinary_id == image_id)
            image = (await self._db_session.exec(statement)).first()
            if not image:
                self._logger.error(f"Image with id: {image_id} was not found on database, delete option cancelled.")
                return None

            await self._db_session.delete(image)
            await self._db_session.commit()
            self._logger.info(f"Image with id: {image_id} was deleted successfuly from database")
        except SQLAlchemyError as e:
            await self._db_session.rollback()
            raise DatabaseException(f"Cannot delete the image with id: {image_id} from database") from e