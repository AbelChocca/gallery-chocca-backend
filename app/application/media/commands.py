from dataclasses import dataclass
from typing import Optional

@dataclass
class UpdateImageCommand:
    id: Optional[int] = None
    owner_id: Optional[int] = None
    image_url: Optional[str] = None
    service_id: Optional[str] = None

    # flags
    to_delete: bool = False