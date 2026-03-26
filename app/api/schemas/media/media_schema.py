from pydantic import BaseModel, ConfigDict, Field

class ReadImage(BaseModel):
    image_url: str
    id: int
    public_id: str
    owner_id: int | None = Field(default=None)
    alt_text: str | None = Field(default=None)

    model_config = ConfigDict(from_attributes=True)

class UpdateImage(BaseModel):
    id: int | None = Field(default=None)
    owner_id: int | None = Field(default=None)
    image_url: str | None = Field(default=None, examples=[None])
    public_id: str | None = Field(default=None, examples=[None])

    # flags
    to_delete: bool = Field(default=False)