"""initialize gc-v1.0.0

Revision ID: a5ab5d9659b7
Revises: 001_postgres_bootstrap
Create Date: 2026-11-12 23:49:07.396393

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'a5ab5d9659b7'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


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