from dataclasses import dataclass 
from app.features.media.entities.image import ImageEntity
from app.features.media.types import ImageType

@dataclass
class MediaImageDTO:
    url: str
    public_id: str

@dataclass(slots=True)
class ReadMediaImageDTO:
    image_url: str
    public_id: str
    alt_text: str | None
    owner_id: int | None
    owner_type: ImageType
    id: int | None = None

    @classmethod
    def from_entity(
        cls,
        image: ImageEntity
    ) -> "ReadMediaImageDTO":
        return cls(
            id=image.id,
            image_url=image.image_url,
            public_id=image.public_id,
            alt_text=image.alt_text,
            owner_id=image.owner_id,
            owner_type=image.owner_type
        )
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "image_url": self.image_url,
            "public_id": self.public_id,
            "alt_text": self.alt_text,
            "owner_id": self.owner_id,
            "owner_type": self.owner_type.value
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ReadMediaImageDTO":
        return cls(
            id=data["id"],
            image_url=data["image_url"],
            public_id=data["public_id"],
            alt_text=data["alt_text"],
            owner_id=data["owner_id"],
            owner_type=ImageType(data["owner_type"])
        )

@dataclass
class UpdateImageCommand:
    id: int | None = None
    owner_id: int | None = None
    image_url: str | None = None
    public_id: str | None = None

    # flags
    to_delete: bool = False
