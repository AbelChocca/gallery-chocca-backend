from sqlalchemy import text
import asyncio

from app.infra.db.config import async_session_factory


CATEGORY_MAPPING = {
    "pant": "PANT",
    "shirt": "SHIRT",
    "short": "SHORT",
    "jacket": "JACKET",
}

FIT_MAPPING = {
    "slim": "SLIM",
    "regular": "REGULAR",
    "relaxed": "RELAXED",
    "straight": "STRAIGHT",
    "tapered": "REGULAR",
    "boxy": "LOOSE",
}


async def migrate_products() -> None:

    async with async_session_factory() as session:

        result = await session.execute(
            text(
                """
                SELECT
                    id,
                    categoria,
                    fit
                FROM product
                ORDER BY id
                """
            )
        )

        products = result.mappings().all()

        print(
            f"Found {len(products)} products to migrate."
        )

        unknown_categories = set()
        unknown_fits = set()

        for product in products:

            category = product["categoria"]
            fit = product["fit"]

            if (
                category is not None
                and category.strip().lower()
                not in CATEGORY_MAPPING
            ):
                unknown_categories.add(category)

            if (
                fit is not None
                and fit.strip().lower()
                not in FIT_MAPPING
            ):
                unknown_fits.add(fit)

        if unknown_categories:
            raise ValueError(
                f"Unknown categories: {unknown_categories}"
            )

        if unknown_fits:
            raise ValueError(
                f"Unknown fits: {unknown_fits}"
            )

        for product in products:

            product_id = product["id"]

            old_category = product["categoria"]
            old_fit = product["fit"]

            new_category = (
                CATEGORY_MAPPING[
                    old_category.strip().lower()
                ]
                if old_category
                else None
            )

            new_fit = (
                FIT_MAPPING[
                    old_fit.strip().lower()
                ]
                if old_fit
                else None
            )

            await session.execute(
                text(
                    """
                    UPDATE product
                    SET
                        categoria = :categoria,
                        fit = :fit
                    WHERE id = :id
                    """
                ),
                {
                    "id": product_id,
                    "categoria": new_category,
                    "fit": new_fit,
                },
            )

            print(
                f"[{product_id}] "
                f"category: {old_category} -> {new_category} | "
                f"fit: {old_fit} -> {new_fit}"
            )

        await session.commit()

        print(
            "Migration completed successfully."
        )


if __name__ == "__main__":
    asyncio.run(migrate_products())