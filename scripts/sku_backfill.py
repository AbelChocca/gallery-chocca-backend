from app.infra.db.unit_of_work import UnitOfWork
from app.infra.db.config import async_session_factory
from app.infra.db.models.model_product import ProductTable, VariantTable
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import asyncio

async def execute():
    async with UnitOfWork(async_session_factory) as uow:
        stmt = (
            select(ProductTable)
            .options(
                selectinload(ProductTable.variants)
                .selectinload(VariantTable.sizes)
            )
        )

        results = await uow.session.execute(stmt)

        for product_table in results.scalars().all():
            base = ''.join(
                s[0].upper()
                for s in product_table.nombre.strip().split()
                if s
            )
            # ya viene con relaciones cargadas
            for variant in product_table.variants:
                for size in variant.sizes:
                    variant_sku = f"{base}-{variant.color[:3].upper()}-{size.size.upper()}"
                    
                    size.sku = variant_sku

        await uow.session.commit()

if __name__ == "__main__":
    asyncio.run(execute())