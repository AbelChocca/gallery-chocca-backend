from pydantic import BaseModel, ConfigDict
from app.api.schemas.user.user_schema import ReadUserSchema
from app.api.schemas.products.schema import GridProductRead
from app.api.schemas.slides.slide_schema import ReadSlideSchema

class _CategoryCount(BaseModel):
    total: int
    category: str

class _RoleCount(BaseModel):
    total: int
    role: str

class _ProductsOverview(BaseModel):
    total: int
    per_category: list[_CategoryCount]
    recent: list[GridProductRead]

class _UsersOverview(BaseModel):
    total: int
    active: int
    inactive: int
    per_role: list[_RoleCount]
    recent: list[ReadUserSchema]

class _SlidesOverview(BaseModel):
    total: int
    active: int
    inactive: int
    recent: list[ReadSlideSchema]

class OverviewSchema(BaseModel):
    admin: ReadUserSchema
    products: _ProductsOverview
    users: _UsersOverview
    slides: _SlidesOverview


    model_config = ConfigDict(from_attributes=True)