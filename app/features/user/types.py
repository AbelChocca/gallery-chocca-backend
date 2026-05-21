from typing import TypedDict

class ActivateAndInactiveUsers(TypedDict):
    active: int
    inactive: int

class UsersPerRole(TypedDict):
    role: str
    total: int

class UsersOverview(TypedDict):
    total_users: int
    sessions_count: ActivateAndInactiveUsers
    users_per_role: list[UsersPerRole]
    last_three_users: list[dict]