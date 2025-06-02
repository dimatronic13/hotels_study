"""update users tables. fix

Revision ID: 4a00e5f370cb
Revises: fd5ea7c09500
Create Date: 2025-06-02 22:58:33.193410

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4a00e5f370cb"
down_revision: Union[str, None] = "fd5ea7c09500"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "users", sa.Column("hashed_password", sa.String(length=200), nullable=False)
    )
    op.drop_column("users", "password")



def downgrade() -> None:
    """Downgrade schema."""

    op.add_column(
        "users",
        sa.Column(
            "password", sa.VARCHAR(length=200), autoincrement=False, nullable=False
        ),
    )
    op.drop_column("users", "hashed_password")

