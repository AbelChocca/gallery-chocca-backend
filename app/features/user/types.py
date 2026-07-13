from enum import StrEnum

class UserRole(StrEnum):
    ADMIN = "admin"

    MANAGER = "manager"

    SELLER = "seller"

    INVENTORY = "inventory"

    ACCOUNTANT = "accountant"

    USER = "user"