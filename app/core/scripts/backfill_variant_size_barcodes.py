import asyncio

from app.infra.db.config import async_session_factory
from app.features.products.models.model_product import VariantSizeTable
from app.features.products.variant_size.variant_size import VariantSize

from sqlalchemy import select

async def backfill_variant_size_barcodes():
    async with async_session_factory() as session:

        result = await session.execute(
            select(VariantSizeTable)
            .where(
                VariantSizeTable.barcode.is_(None)
            )
        )

        variant_sizes = result.scalars().all()

        print(
            f"Encontrados {len(variant_sizes)} variant sizes sin barcode"
        )

        for variant_size in variant_sizes:
            if variant_size.barcode: 
                continue
            
            variant_size.barcode = VariantSize.generate_barcode()

        await session.commit()

        print("Barcodes generados correctamente")


if __name__ == "__main__":
    asyncio.run(backfill_variant_size_barcodes())