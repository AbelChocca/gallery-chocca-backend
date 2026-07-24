from app.features.products.variant_size.variant_size_route import variant_size_router

from fastapi import status

@variant_size_router.post(
    "/add-materials/{variant_size}",
    status_code=status.HTTP_201_CREATED,
    # response_model=AddVariantSizeMaterials
)
async def add_materials_to_variant_size(
    
):
    pass