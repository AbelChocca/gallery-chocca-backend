from sqlmodel import SQLModel, DateTime, Column, Index, text, Field, Boolean
from datetime import datetime

# Modelo SQL para Admin
class UserTable(SQLModel, table=True):
    __table_args__ = (
        Index(
            "ix_user_nombre_trgm",
            "nombre",
            postgresql_using="gin",
            postgresql_ops={"nombre": "gin_trgm_ops"},
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=50, unique=True)
    email: str = Field(index=True, unique=True)
    role: str = Field(default='user',index=True, max_length=20)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=text('now()'), nullable=False)
        )
    is_active: bool = Field(
        sa_column=Column(Boolean, default=True, nullable=False)
    )
    hashed_password: str
