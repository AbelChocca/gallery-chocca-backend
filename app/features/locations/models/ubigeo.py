from sqlmodel import Field, SQLModel
from sqlalchemy import CheckConstraint


class UbigeoTable(SQLModel, table=True):
    __tablename__ = "ubigeos"

    __table_args__ = (
        CheckConstraint(
            "char_length(code) = 6",
            name="ck_ubigeos_code_length",
        ),
    )

    code: str = Field(
        primary_key=True,
        max_length=6,
    )

    department: str = Field(
        max_length=100,
        nullable=False,
        index=True,
    )

    province: str = Field(
        max_length=100,
        nullable=False,
        index=True,
    )

    district: str = Field(
        max_length=100,
        nullable=False,
        index=True,
    )

    city_name: str | None = Field(
        default=None,
        max_length=150,
    )