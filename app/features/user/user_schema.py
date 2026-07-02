from pydantic import BaseModel, ConfigDict
from app.features.user.types import UserRole
from typing import  List
from datetime import datetime
from app.shared.pagination.schema import PaginationResponseSchema

class UpdateUserRoleSchema(BaseModel):
    role: UserRole

class ReadUserSchema(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    created_at: datetime | None = None
    role: UserRole

    model_config = ConfigDict(from_attributes=True)

class GetUsersResponseSchema(BaseModel):
    users: List[ReadUserSchema]
    pagination: PaginationResponseSchema
    total_items: int