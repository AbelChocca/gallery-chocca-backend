from typing import Optional

class ImageEntity:
    def __init__(
            self,
            image_url: str,
            owner_type: str,
            service_id: str,
            owner_id: Optional[int] = None,
            id: Optional[int] = None,
            alt_text: Optional[str] = None
            ):
        self.image_url: str = image_url
        self.service_id: str = service_id
        self.owner_type: str = owner_type
        self.owner_id: int = owner_id or None
        self.id: Optional[int] = id or None
        self.alt_text: Optional[str] = alt_text or None


    def set_owner_id(self, id: int) -> None:
        self.owner_id = id
    def set_id(self, new_id: int) -> None:
        self.id = new_id