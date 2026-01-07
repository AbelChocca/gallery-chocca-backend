from typing import Optional

class ImageEntity:
    def __init__(
            self,
            image_url: str,
            owner_type: str,
            owner_id: int,
            id: Optional[int] = None,
            alt_text: Optional[str] = None
            ):
        self._image_url: str = image_url
        self._owner_type: str = owner_type
        self._owner_id: int = owner_id
        self._id: Optional[int] = id or None
        self._alt_text: Optional[str] = alt_text or None