"""room added

Revision ID: 6c43be5c3a8e
Revises: f0087a716998
Create Date: 2025-05-31 00:05:02.826147

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6c43be5c3a8e"
down_revision: Union[str, None] = "f0087a716998"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hotel_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["hotel_id"],
            ["hotels.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
   


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("rooms")
   
