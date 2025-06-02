"""update users tables. uniq email

Revision ID: fd5ea7c09500
Revises: f801435adc62
Create Date: 2025-06-02 22:53:12.643759

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fd5ea7c09500"
down_revision: Union[str, None] = "f801435adc62"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_unique_constraint(None, "users", ["email"])



def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(None, "users", type_="unique")

