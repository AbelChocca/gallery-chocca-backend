from dataclasses import dataclass, field

@dataclass(slots=True)
class CountUsersPerRoleDTO:
    role: str
    total: int

@dataclass(slots=True)
class UsersOverviewDTO:
    total: int = 0
    active: int = 0
    inactive: int = 0
    per_role: list[CountUsersPerRoleDTO] = field(default_factory=list)
    recent: list[dict] = field(default_factory=list)