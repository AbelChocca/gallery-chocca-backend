from pydantic import BaseModel, Field, ConfigDict

class PaginationSchema(BaseModel):
    page: int = Field(1, ge=1, title="Page")
    limit: int = Field(20, gt=0, le=100, title="Limit")

class ProductRelatedPaginationSchema(PaginationSchema):
    limit: int = Field(3, gt=0, le=100, title="Limit")

class PaginationResponseSchema(BaseModel):
    total_pages: int
    current_page: int

    model_config = ConfigDict(from_attributes=True)