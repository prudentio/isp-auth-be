"""create_family_card_table

Revision ID: 8b7d27a14207
Revises: 34009ac5e93f
Create Date: 2025-08-25 14:23:07.196976

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b7d27a14207'
down_revision: Union[str, None] = '34009ac5e93f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  op.execute("PRAGMA journal_mode=WAL;")
    
  op.create_table(
        'family_cards',
        sa.Column('id', sa.Text(), primary_key=True, nullable=False),
  )


def downgrade() -> None:
    op.drop_table('family_cards')

