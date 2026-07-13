from pydantic import BaseModel, ConfigDict, Field
from app.features.user.user_schema import ReadUserSchema
from app.features.products.schema import GridProductRead
from app.features.slides.slide_schema import ReadSlideSchema

class _CategoryCount(BaseModel):
    total: int
    category: str

class _RoleCount(BaseModel):
    total: int
    role: str

class _ProductsOverview(BaseModel):
    total: int
    per_category: list[_CategoryCount] = Field(default_factory=list)
    recent: list[GridProductRead] = Field(default_factory=list)

class _UsersOverview(BaseModel):
    total: int
    active: int
    inactive: int
    per_role: list[_RoleCount] = Field(default_factory=list)
    recent: list[ReadUserSchema] = Field(default_factory=list)

class _SlidesOverview(BaseModel):
    total: int
    active: int
    inactive: int
    recent: list[ReadSlideSchema] = Field(default_factory=list)

class OverviewSchema(BaseModel):
    admin: ReadUserSchema
    products: _ProductsOverview
    users: _UsersOverview
    slides: _SlidesOverview


    model_config = ConfigDict(from_attributes=True)