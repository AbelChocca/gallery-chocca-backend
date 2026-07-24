from app.features.inventory.use_cases.get_inventory_products import (
    GetInventoryProductsUseCase,
)

from app.features.media.service import (
    MediaService,
)

from app.features.media.dependency import (
    get_media_service,
)

from app.shared.pagination.pagination_service import PaginationService, get_pagination_service

from app.features.inventory.use_cases.get_inventory_product_detail import (
    GetInventoryProductDetailUseCase,
)

from app.features.inventory.use_cases.update_inventory_locations import (
    UpdateInventoryLocationsUseCase,
)

from app.features.inventory.dependencies.services import (
    get_inventory_service,
    get_inventory_location_service,
)

from app.features.inventory.services.inventory_service import (
    InventoryService,
)

from app.features.inventory.services.inventory_location_service import (
    InventoryLocationService,
)

from app.features.inventory.use_cases.get_inventory_materials import (
    GetInventoryMaterialsUseCase,
)

from app.features.inventory.use_cases.get_inventory_material_detail import (
    GetInventoryMaterialDetailUseCase,
)

from app.features.material.service import (
    MaterialService,
)

from app.features.material.dependency import (
    get_material_service,
)

from fastapi import Depends

def get_inventory_products_use_case(
    inventory_service: InventoryService = Depends(
        get_inventory_service,
    ),
    media_service: MediaService = Depends(
        get_media_service,
    ),
    pagination_service: PaginationService = Depends(get_pagination_service)
) -> GetInventoryProductsUseCase:

    return GetInventoryProductsUseCase(
        inventory_service=inventory_service,
        media_service=media_service,
        pagination_service=pagination_service
    )

def get_update_inventory_locations_use_case(
    inventory_service: InventoryService = Depends(
        get_inventory_service,
    ),
    inventory_location_service: InventoryLocationService = Depends(
        get_inventory_location_service,
    ),
) -> UpdateInventoryLocationsUseCase:

    return UpdateInventoryLocationsUseCase(
        inventory_service=inventory_service,
        inventory_location_service=inventory_location_service,
    )

def get_inventory_product_detail_use_case(
    inventory_service: InventoryService = Depends(
        get_inventory_service,
    ),
    media_service: MediaService = Depends(
        get_media_service,
    ),
) -> GetInventoryProductDetailUseCase:

    return GetInventoryProductDetailUseCase(
        inventory_service=inventory_service,
        media_service=media_service,
    )

def get_inventory_materials_use_case(
    inventory_service: InventoryService = Depends(
        get_inventory_service,
    ),
    media_service: MediaService = Depends(
        get_media_service,
    ),
    pagination_service: PaginationService = Depends(
        get_pagination_service,
    ),
) -> GetInventoryMaterialsUseCase:

    return GetInventoryMaterialsUseCase(
        inventory_service=inventory_service,
        media_service=media_service,
        pagination_service=pagination_service,
    )

def get_inventory_material_detail_use_case(
    inventory_service: InventoryService = Depends(
        get_inventory_service,
    ),
    material_service: MaterialService = Depends(
        get_material_service,
    ),
    media_service: MediaService = Depends(
        get_media_service,
    ),
) -> GetInventoryMaterialDetailUseCase:

    return GetInventoryMaterialDetailUseCase(
        inventory_service=inventory_service,
        material_service=material_service,
        media_service=media_service,
    )