from pathlib import Path
from app.features.products.types import BrandType

from app.core.constants.paths import BRANDS_DIR

class BrandAssets:
    @staticmethod
    def logo(brand: BrandType) -> Path:
        return BRANDS_DIR / brand.value / "logo.png"