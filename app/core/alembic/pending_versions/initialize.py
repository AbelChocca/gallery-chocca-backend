"""Bootstrap PostgreSQL objects."""

from alembic import op

revision = "001_postgres_bootstrap"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        "CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public"
    )
    op.execute(
        "CREATE EXTENSION IF NOT EXISTS unaccent WITH SCHEMA public"
    )

    op.execute("""
        CREATE SEQUENCE IF NOT EXISTS public.order_number_seq
        AS BIGINT START WITH 1 INCREMENT BY 1
        MINVALUE 1 NO MAXVALUE CACHE 1 NO CYCLE
    """)

    op.execute("""
        CREATE SEQUENCE IF NOT EXISTS public.complaint_number_seq
        AS BIGINT START WITH 1 INCREMENT BY 1
        MINVALUE 1 NO MAXVALUE CACHE 1 NO CYCLE
    """)


def downgrade() -> None:
    op.execute(
        "DROP SEQUENCE IF EXISTS public.complaint_number_seq"
    )
    op.execute(
        "DROP SEQUENCE IF EXISTS public.order_number_seq"
    )