from sqlmodel import SQLModel, Field, Column, Relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Boolean, Float, text
from typing import Optional, List
from sqlalchemy.orm import Mapped


class ProductTable(SQLModel, table=True):
    __tablename__ = "product"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(nullable=False, unique=True)
    descripcion: str
    marca: str = Field(nullable=False, index=True)
    categoria: str = Field(max_length=30, index=True)  # Ej: "pantalon", "camisa"
    modelo: Optional[str] = Field(default=None, max_length=20, index=True)  # Ej: "jean", "drill"
    precio: float
    slug: Optional[str] = Field(default=None)
    descuento: Optional[float] = Field(sa_column=Column(Float, server_default=text('0.00')))
    promocion: Optional[bool] = Field(sa_column=Column(Boolean, server_default=text('false'), index=True))

    variants: Mapped[List['VariantColorTable']] = Relationship(
        back_populates='product',
        sa_relationship_kwargs={
            'cascade': 'all, delete-orphan',
            'lazy': 'selectin'
        }
    )


class VariantColorTable(SQLModel, table=True):
    __tablename__ = "variant"

    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: Optional[int] = Field(foreign_key='product.id')
    color: str
    tallas: List[str] = Field(default_factory=list, sa_column=Column(JSONB))

    product: Mapped[Optional[ProductTable]] = Relationship(back_populates='variants')