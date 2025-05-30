"""fix named

Revision ID: f0087a716998
Revises: 64d177c7a4e0
Create Date: 2025-05-30 23:48:18.730570

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0087a716998'
down_revision: Union[str, None] = '64d177c7a4e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column('hotels', sa.Column('title', sa.String(length=100), nullable=False))
    op.drop_column('hotels', 'tittle')



def downgrade() -> None:
    """Downgrade schema."""

    op.add_column('hotels', sa.Column('tittle', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
    op.drop_column('hotels', 'title')

