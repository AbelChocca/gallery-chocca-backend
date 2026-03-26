from datetime import datetime, timezone

from app.core.exceptions import ValidationError

class User:
    def __init__(
            self,
            name: str,
            email: str,
            hashed_password: str,
            is_active: bool = True,
            created_at: datetime = datetime.now(timezone.utc),
            role: str = 'user',
            id: int|None = None
            ):
        self.id = id
        self.name = name
        self.email = email
        self.role = role
        self.is_active = is_active
        self.created_at = created_at
        self.hashed_password = hashed_password

    def toggle_active(self, toggle_bool: bool) -> None:
        self.is_active = toggle_bool

    def change_email(self, new_email: str) -> None:
        if self.email == new_email:
            raise ValidationError(
                "New email must not be equal to previous email",
                {
                    "entity": "User",
                    "field": "email",
                    "event": "change_email"
                }
            )

        self.email = new_email

    def change_password(self, new_hashed_password: str)-> None:
        self.hashed_password = new_hashed_password
        
    @property
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "role": self.role
        }