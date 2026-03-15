from dataclasses import dataclass
from typing import List
from datetime import datetime
from app.shared.dtos import PaginationResponseDTO

@dataclass(frozen=True)
class ReadUserDTO:
    nombre: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    id: int | None = None

@dataclass
class GetUsersResponseDTO:
    users: List[ReadUserDTO]
    pagination: PaginationResponseDTO

@dataclass
class RegisterUserCommand:
    nombre: str
    email: str
    password: str
    role: str

@dataclass
class LoginUserCommand:
    email: str
    password: str