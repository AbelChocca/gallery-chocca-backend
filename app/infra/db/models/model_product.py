from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint, Index, Column, Numeric, text, Boolean, Enum
from app.features.products.types import BrandType, CategoryType, FitType
from sqlalchemy.orm import Mapped
from decimal import Decimal

class ProductTable(SQLModel, table=True):
    __tablename__ = "product"
    __table_args__ = (
        Index(
            "ix_product_nombre_trgm",
            "nombre",
            postgresql_using="gin",
            postgresql_ops={"nombre": "gin_trgm_ops"},
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(nullable=False, unique=True)
    descripcion: str
    brand: BrandType = Field(sa_column=Column(Enum(BrandType, name="brand_type"), nullable=False))
    category: CategoryType = Field(sa_column=Column(Enum(CategoryType, name="category_type"), index=True))
    fit: FitType | None = Field(default=None, sa_column=Column(Enum(FitType, name="fit_type")))
    slug: str | None = Field(default=None)
    is_active: bool = Field(default=True, sa_column=Column(Boolean, server_default=text("true")))

    base_price: Decimal = Field(
        default=Decimal('0.00'),
        sa_column=Column(
            Numeric(10, 2),
            nullable=False,
            server_default=text('0.00')
        )
    )

    variants: Mapped[list['VariantTable']] = Relationship(
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

    id: int | None = Field(default=None, primary_key=True)
    product_id: int | None = Field(foreign_key='product.id')
    color: str

    product: Mapped[ProductTable | None] = Relationship(back_populates='variants')

    sizes: Mapped[list['VariantSizeTable']] = Relationship(
        back_populates="variant",
        sa_relationship_kwargs={
            'cascade': 'all, delete-orphan',
            'lazy': 'selectin'
        }
    )

class VariantSizeTable(SQLModel, table=True):
    __tablename__ = "variant_size"
    __table_args__ = (
        UniqueConstraint("variant_id", "size", name="uq_variant_size"),
    )

    id: int | None = Field(default=None, primary_key=True)
    variant_id: int = Field(foreign_key="variant.id")
    size: str

    stock: int = Field(default=0, ge=0)
    sku: str

    variant: Mapped[VariantTable | None] = Relationship(back_populates="sizes")
