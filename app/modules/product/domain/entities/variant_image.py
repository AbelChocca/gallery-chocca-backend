from typing import Optional

class VariantImage:
    def __init__(
            self,
            url: str,
            cloudinary_id: str,
            id: Optional[int] = None,
            variant_id: Optional[int] = None
            ):
        self.url: str = url
        self.cloudinary_id: str = cloudinary_id
        self.id: int = id
        self.variant_id: int = variant_id