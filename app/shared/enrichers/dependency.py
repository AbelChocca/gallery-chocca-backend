from app.features.media.dependency import get_media_service
from app.features.media.service import MediaService
from app.shared.enrichers.product_enricher import ProductEnricher

from fastapi import Depends

def get_product_enricher(
    media_service: MediaService = Depends(get_media_service),
) -> ProductEnricher:

    return ProductEnricher(
        media_service=media_service,
    )