"""add refunded to order status

Revision ID: c66d967b5841
Revises: a5cc7c0d1a51
Create Date: 2026-08-04 21:56:07.435788

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c66d967b5841'
down_revision: Union[str, Sequence[str], None] = 'a5cc7c0d1a51'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE orderstatus ADD VALUE 'refunded'")


def downgrade() -> None:
    """Downgrade schema."""
    pass
