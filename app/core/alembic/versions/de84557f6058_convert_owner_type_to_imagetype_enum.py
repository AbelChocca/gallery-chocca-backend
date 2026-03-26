from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "de84557f6058"
down_revision = "0e6eadc205ca"

image_owner_type_enum = postgresql.ENUM(
    "variant",
    "slide",
    name="image_owner_type",
    create_type=False,
)

def upgrade():
    image_owner_type_enum.create(op.get_bind(), checkfirst=True)

    op.alter_column(
        "image",
        "owner_type",
        type_=image_owner_type_enum,
        postgresql_using="owner_type::image_owner_type",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )

def downgrade():
    op.alter_column(
        "image",
        "owner_type",
        type_=sa.VARCHAR(),
        existing_type=image_owner_type_enum,
        nullable=False,
    )

    image_owner_type_enum.drop(op.get_bind(), checkfirst=True)
