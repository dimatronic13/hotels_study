"""users tables

Revision ID: c1760344b681
Revises: 6c43be5c3a8e
Create Date: 2025-06-02 22:04:46.769185

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



revision: str = "c1760344b681"
down_revision: Union[str, None] = "6c43be5c3a8e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )



def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("users")

