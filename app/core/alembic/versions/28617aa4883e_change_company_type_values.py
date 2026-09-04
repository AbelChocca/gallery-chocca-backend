"""change company type values

Revision ID: 28617aa4883e
Revises: 71bfa48d7078
Create Date: 2026-08-28 22:30:22.161620

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "28617aa4883e"
down_revision: Union[str, Sequence[str], None] = "71bfa48d7078"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Change CHOCCA to CREATOR."""
    op.execute(
        """
        ALTER TYPE company_type
        RENAME VALUE 'CHOCCA' TO 'CREATOR'
        """
    )


def downgrade() -> None:
    """Restore CREATOR to CHOCCA."""
    op.execute(
        """
        ALTER TYPE company_type
        RENAME VALUE 'CREATOR' TO 'CHOCCA'
        """
    )