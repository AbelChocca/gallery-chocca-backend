from sqlmodel import SQLModel, Field, Column, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM
from app.domain.media.media_dto import ImageType
from sqlalchemy import Index, text

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
            "uq_only_one_primary_per_owner",
            "owner_type",
            "owner_id",
            unique=True,
            postgresql_where=text("is_primary = true")
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    public_id: str = Field(nullable=False)

    image_url: str = Field(nullable=False)
    alt_text: str | None = Field(default=None)

    owner_type: ImageType = Field(
        sa_column=Column(
            ENUM(ImageType, name="image_owner_type", create_type=False),
            nullable=False
            )
        )
    owner_id: int = Field(nullable=False)
    is_primary: bool | None = Field(default=None, nullable=True)