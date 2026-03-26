from dataclasses import dataclass

@dataclass
class UpdateVariantSizeCommand:
    size: str | None = None
    id: int | None = None
    variant_id: int | None = None

    to_delete: bool = False

@dataclass
class PublishVariantSizeCommand:
    size: str