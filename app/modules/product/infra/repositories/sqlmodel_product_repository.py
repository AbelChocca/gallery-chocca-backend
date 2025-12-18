from app.modules.product.domain.repositories.repository_product import ProductRepository
from app.modules.product.domain.entities.product import Product
from app.modules.product.infra.models.product_model import ProductTable, VariantColorTable, VariantImageTable
from app.modules.product.infra.mappers.product_mapper import ProductMapper
from app.modules.product.infra.exceptions import ProductNotFound, VariantImageNotFound, CannotDeleteVariantImage, CannotDeleteVariantProduct, VariantProductNotFound

from app.modules.product.domain.dto.product_dto import FilterSchemaDTO

from app.shared.exceptions.infraestructure_exception import DatabaseException
from app.core.log.logger_repository import LoggerRepository

from typing import Optional, List
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import func

class PostgresProductRepository(ProductRepository):
    def __init__(self, db_session: AsyncSession, logger: LoggerRepository):
        self.db_session = db_session
        self.logger = logger

    async def _get_product_table_or_raise(self, product_id: int) -> ProductTable:
        product_db = await self.db_session.get(ProductTable, product_id)
        if not product_db:
            raise ProductNotFound(f"Product with id={product_id} wasn't found")
        return product_db
    
    async def _get_product_table_or_none(self, product_id: int) -> Optional[ProductTable]:
        return await self.db_session.get(ProductTable, product_id)

    async def save(self, product: Product) -> Product:
        try:
            existing = None
            if product.id is not None:
                existing = await self._get_product_table_or_none(product.id)

            product_table = ProductMapper.to_db_model(product, existing)

            self.db_session.add(product_table)
            await self.db_session.commit()
            await self.db_session.refresh(product_table)
            return ProductMapper.to_entity(product_table)
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            self.logger.error(f"Fatal error to save in database: {str(e)}")
            raise DatabaseException("Cannot save product to database.") from e

    async def get_by_id(self, product_id: int) -> Product:
        product_db = await self.db_session.get(ProductTable, product_id)
        if not product_db:
            raise ProductNotFound(f"Product with id: {product_id} wasn't found.")
        return ProductMapper.to_entity(product_db)
    
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
        result = await self.db_session.exec(stmt)
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

        res = (await self.db_session.exec(stmt)).all()

        products = [
            ProductMapper.to_entity(product_table)
            for product_table in res
        ]
        return products
        

    async def delete_by_id(self, id: int) -> None:
        try:
            product = await self._get_product_table_or_raise(id)

            await self.db_session.delete(product)
            await self.db_session.commit()
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise DatabaseException(f"Cannot delete the product with id: {id} from database") from e
        
    async def delete_image_by_id(self, cloudinary_id: str) -> None:
        stmt = select(VariantImageTable).where(VariantImageTable.cloudinary_id == cloudinary_id)
        image = (await self.db_session.exec(stmt)).first()
        if not image:
            raise VariantImageNotFound(f"Image with id:{cloudinary_id} was not found.")
        
        query = (
            select(VariantColorTable)
            .options(selectinload(VariantColorTable.imagenes))
            .where(VariantColorTable.id == image.variant_id)
        )
        res = await self.db_session.exec(query)
        variant = res.first()
        
        if len(variant.imagenes) <= 1:
            raise CannotDeleteVariantImage("Cannot delete image from database, need atleast two images to delete one")
        try:
            await self.db_session.delete(image)
            await self.db_session.commit()
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise DatabaseException("Cannot delete the image from database") from e
        
    async def delete_variant_by_id(self, variant_id: int) -> None:
        variant = await self.db_session.get(VariantColorTable, variant_id)
        if not variant:
            raise VariantProductNotFound(f"Variant with id: {variant_id} was not found.")
        
        query = (
            select(ProductTable)
            .options(selectinload(ProductTable.variants))
            .where(ProductTable.id == variant.product_id)
        )
        result = await self.db_session.exec(query)
        product = result.first()
        if not product:
            raise DatabaseException("Product not found in this variant.")
        if len(product.variants) <= 1:
            raise CannotDeleteVariantProduct("You need atleast two variants to delete one.")

        try:
            await self.db_session.delete(variant)
            await self.db_session.commit()
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise DatabaseException("Cannot delete the variant from database") from e