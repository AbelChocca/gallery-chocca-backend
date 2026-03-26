from typing import Dict, Any
from app.domain.media.media_dto import ImageType

from app.core.exceptions import ValidationError

class ImageEntity:
    def __init__(
            self,
            image_url: str,
            owner_type: ImageType,
            public_id: str,
            owner_id: int | None = None,
            id: int | None = None,
            alt_text: str | None = None
            ):
        
        if not image_url:
            raise ValidationError(
                "Image must has an image_url",
                {
                    "entity": "ImageEntity",
                    "event": 'image_instance',
                }
                )
        if not public_id:
            raise ValidationError(
                    "Image must has an public_id",
                    {
                        "entity": "ImageEntity",
                        "event": 'image_instance',
                    }
                    )
        
        self.image_url: str = image_url
        self._public_id: str = public_id
        self.owner_type: ImageType = owner_type
        self._owner_id: int = owner_id or None
        self._id: int | None = id or None
        self.alt_text: str | None = alt_text or None

    @property
    def owner_id(self) -> int | None:
        return self._owner_id

    @owner_id.setter
    def owner_id(self, new_owner_id: int) -> None:
        self._owner_id = new_owner_id

    @property
    def id(self) -> int | None:
        return self._id

    @id.setter
    def id(self, new_id: int) -> None:
        self._id = new_id

    @property
    def public_id(self) -> str:
        return self._public_id
    
    @public_id.setter
    def public_id(self, new_public_id: str) -> None:
        if not isinstance(new_public_id, str):
            raise ValidationError(
                "'new_public_id' must be a string",
                {
                    "entity": "ImageEntity",
                    "event": "public_id.setter",
                    "invalid_prop_type": type(new_public_id).__name__
                }
                )
        self._public_id = new_public_id

    @property
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "image_url": self.image_url,
            "public_id": self.public_id,
            "alt_text": self.alt_text,
            "owner_id": self.owner_id,
            "owner_type": self.owner_type
        }

    def set_alt_text(self, args: Dict[str, str]) -> None:
        if not isinstance(args, dict):
            raise ValidationError(
                "'args' must be a dict",
                {
                    "entity": "ImageEntity",
                    "event": "set_alt_text",
                    "invalid_args_type": type(args).__name__
                }
                )
        values = []
        for key, value in args.items():
            if not isinstance(value, str):
                raise ValidationError(
                    f"'{key}' must be a string",
                    {
                        "entity": "ImageEntity",
                        "event": "set_alt_text",
                        "invalid_key_type": type(key).__name__
                    }
                )
            values.append(value.strip())
        self.alt_text = ' '.join(values)
        
    def __str__(self):
        return f"Public: {self.public_id}"