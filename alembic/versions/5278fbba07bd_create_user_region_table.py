"""create user region table

Revision ID: 5278fbba07bd
Revises: 0914482d7527
Create Date: 2025-04-14 15:22:51.476346

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5278fbba07bd'
down_revision: Union[str, None] = '0914482d7527'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_regions",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("region_id", sa.Text(), sa.ForeignKey("regions.id", ondelete="CASCADE"), nullable=False)
    )

    op.create_index('ix_user_regions_id', 'user_regions', ['id']) 


def downgrade() -> None:
    op.drop_index('ix_user_regions_id', table_name='user_regions')
    op.drop_table('user_regions')