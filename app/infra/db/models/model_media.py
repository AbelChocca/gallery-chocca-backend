from sqlmodel import SQLModel, Field, Column, UniqueConstraint, Index
from typing import Optional
from sqlalchemy.dialects.postgresql import ENUM
from app.domain.media.media_dto import ImageType

class MediaImageTable(SQLModel, table=True):
    __tablename__ = "image"
    __table_args__ = (
        UniqueConstraint(
            "owner_type",
            "owner_id",
            "public_id",
            name="uq_image_owner_type_owner_id_public_id"
        ),
        Index(
            "ix_image_owner",
            "owner_type",
            "owner_id"
        )
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    public_id: str = Field(nullable=False, index=True)

    image_url: str = Field(nullable=False)
    alt_text: Optional[str] = Field(default=None)

    owner_type: ImageType = Field(
        sa_column=Column(
            ENUM(ImageType, name="image_owner_type", create_type=False),
            index=True,
            nullable=False
            )
        )
    owner_id: int = Field(nullable=False)