from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint, Index
from typing import Optional, List
from sqlalchemy.orm import Mapped

class ProductTable(SQLModel, table=True):
    __tablename__ = "product"
    __table_args__ = (
        Index(
            "ix_product_nombre_trgm",
            "nombre",
            postgresql_using="gin",
            postgresql_ops={"nombre": "gin_trgm_ops"},
        ),
        Index(
            "ix_product_category_model_family",
            "categoria",
            "model_family"
        )
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(nullable=False, unique=True)
    descripcion: str
    marca: str = Field(nullable=False, index=True)
    categoria: str = Field(max_length=30) 
    model_family: str = Field(max_length=50) 
    fit: Optional[str] = Field(default=None, max_length=20)
    slug: Optional[str] = Field(default=None)

    variants: Mapped[List['VariantTable']] = Relationship(
        back_populates='product',
        sa_relationship_kwargs={
            'cascade': 'all, delete-orphan',
            'lazy': 'selectin'
        }
    )

class VariantTable(SQLModel, table=True):
    __tablename__ = "variant"
    __table_args__ = (
        UniqueConstraint("product_id", "color", name="uq_variant_product_color"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: Optional[int] = Field(foreign_key='product.id')
    color: str

    product: Mapped[Optional[ProductTable]] = Relationship(back_populates='variants')

    sizes: Mapped[List['VariantSizeTable']] = Relationship(
        back_populates="variant",
        sa_relationship_kwargs={
            'cascade': 'all, delete-orphan',
            'lazy': 'selectin'
        }
    )

class VariantSizeTable(SQLModel, table=True):
    __tablename__ = "variant_size"
    __table_args__ = (
        Index("ix_variant_size_size_variant_id", "size", "variant_id"),
        UniqueConstraint("variant_id", "size", name="uq_variant_size")
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    variant_id: int = Field(foreign_key="variant.id")
    size: str

    variant: Mapped[Optional[VariantTable]] = Relationship(back_populates="sizes")
