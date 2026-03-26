"""addd new unique constraint and compose index on product and media_image table

Revision ID: 839a9ff11bea
Revises: 4d986d598b1e
Create Date: 2026-02-12 01:31:51.732310

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '839a9ff11bea'
down_revision: Union[str, Sequence[str], None] = '4d986d598b1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""

    # ============================================================
    # 1) IMAGE TABLE
    # ============================================================
    op.add_column(
        'image',
        sa.Column('public_id', sa.String(), nullable=True)
    )   
    op.execute("UPDATE image SET public_id = service_id WHERE public_id IS NULL")
    op.alter_column("image", "public_id", existing_type=sa.String(), nullable=False)

    op.drop_index(op.f('ix_image_owner_id'), table_name='image')
    op.create_index(
        'ix_image_owner',
        'image',
        ['owner_type', 'owner_id'],
        unique=False
    )
    op.create_unique_constraint(
        'uq_image_owner_type_owner_id_public_id',
        'image',
        ['owner_type', 'owner_id', 'public_id']
    )
    op.drop_column('image', 'service_id')

    # ============================================================
    # 2) PRODUCT TABLE
    # ============================================================
    op.add_column(
        'product',
        sa.Column('model_family', sa.String(length=50), nullable=True, server_default="unknown")
    )
    op.add_column(
        'product',
        sa.Column('fit', sa.String(length=20), nullable=True)
    )

    op.execute("UPDATE product SET fit = modelo WHERE fit IS NULL")

    op.drop_index(op.f('ix_product_categoria'), table_name='product')
    op.drop_index(op.f('ix_product_modelo'), table_name='product')
    op.create_index(
        'ix_product_category_model_family',
        'product',
        ['categoria', 'model_family'],
        unique=False
    )
    op.create_index(
        'ix_product_nombre_trgm',
        'product',
        ['nombre'],
        unique=False,
        postgresql_using='gin',
        postgresql_ops={'nombre': 'gin_trgm_ops'}
    )
    op.drop_column('product', 'modelo')

    # ============================================================
    # 3) USERTABLE
    # ============================================================
    op.alter_column(
        'usertable',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_server_default=sa.text('now()')
    )
    op.create_index(
        'ix_user_nombre_trgm',
        'usertable',
        ['nombre'],
        unique=False,
        postgresql_using='gin',
        postgresql_ops={'nombre': 'gin_trgm_ops'}
    )

    # ============================================================
    # 4) VARIANT_SIZE TABLE
    # ============================================================
    op.alter_column(
        'variant_size',
        'variant_id',
        existing_type=sa.INTEGER(),
        nullable=False
    )
    op.create_index(
        'ix_variant_size_size_variant_id',
        'variant_size',
        ['size', 'variant_id'],
        unique=False
    )
    op.create_unique_constraint(
        'uq_variant_size',
        'variant_size',
        ['variant_id', 'size']
    )

def downgrade() -> None:
    """Downgrade schema."""

    # ============================================================
    # 1) VARIANT_SIZE TABLE
    # ============================================================
    op.drop_constraint('uq_variant_size', 'variant_size', type_='unique')
    op.drop_index('ix_variant_size_size_variant_id', table_name='variant_size')
    op.alter_column(
        'variant_size',
        'variant_id',
        existing_type=sa.INTEGER(),
        nullable=True
    )
    op.drop_column("image", "public_id")

    # ============================================================
    # 2) USERTABLE
    # ============================================================
    op.drop_index(
        'ix_user_nombre_trgm',
        table_name='usertable',
        postgresql_using='gin',
        postgresql_ops={'nombre': 'gin_trgm_ops'}
    )
    op.alter_column(
        'usertable',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_server_default=sa.text('now()')
    )

    # ============================================================
    # 3) PRODUCT TABLE
    # ============================================================
    op.add_column(
        'product',
        sa.Column('modelo', sa.VARCHAR(length=20), autoincrement=False, nullable=True)
    )
    op.execute("UPDATE product SET modelo = fit WHERE modelo IS NULL")

    op.drop_index(
        'ix_product_nombre_trgm',
        table_name='product',
        postgresql_using='gin',
        postgresql_ops={'nombre': 'gin_trgm_ops'}
    )
    op.drop_index('ix_product_category_model_family', table_name='product')
    op.create_index(op.f('ix_product_modelo'), 'product', ['modelo'], unique=False)
    op.create_index(op.f('ix_product_categoria'), 'product', ['categoria'], unique=False)
    
    op.drop_column('product', 'fit')
    op.drop_column('product', 'model_family')

    # ============================================================
    # 4) IMAGE TABLE
    # ============================================================
    op.add_column("image", sa.Column("service_id", sa.String(), nullable=True))

    op.execute("UPDATE image SET service_id = public_id WHERE service_id IS NULL")

    op.alter_column("image", "service_id", existing_type=sa.String(), nullable=False)

    op.drop_constraint('uq_image_owner_type_owner_id_public_id', 'image', type_='unique')
    op.drop_index('ix_image_owner', table_name='image')
    op.create_index(op.f('ix_image_owner_id'), 'image', ['owner_id'], unique=False)

    op.drop_column('image', 'public_id')
