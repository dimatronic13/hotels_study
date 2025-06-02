"""update users tables

Revision ID: f801435adc62
Revises: c1760344b681
Create Date: 2025-06-02 22:07:59.869940

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



revision: str = "f801435adc62"
down_revision: Union[str, None] = "c1760344b681"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "users", sa.Column("firstname", sa.String(length=200), nullable=False)
    )
    op.add_column("users", sa.Column("lastname", sa.String(length=200), nullable=False))
    op.add_column("users", sa.Column("nickname", sa.String(length=200), nullable=False))



def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("users", "nickname")
    op.drop_column("users", "lastname")
    op.drop_column("users", "firstname")

