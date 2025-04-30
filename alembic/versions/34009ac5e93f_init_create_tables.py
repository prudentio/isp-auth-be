"""init create tables

Revision ID: 34009ac5e93f
Revises: 
Create Date: 2025-04-24 07:33:28.335334

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34009ac5e93f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("PRAGMA journal_mode=WAL;")
    
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('username', sa.Text(), nullable=False, unique=True),
        sa.Column('password', sa.Text(), nullable=False),
    )

    op.execute(""" 
        INSERT INTO users (id, username, password) 
        VALUES (
            1, 
            'admin', 
            '$argon2i$v=19$m=16,t=2,p=1$UU5tWVFZZ1ZFVHFCV1R1bw$3neLY/prgGXzYeIZK5InDw'
        ) 
    """)

    op.create_table(
        'regions',
        sa.Column('id', sa.Text(), primary_key=True, nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('level', sa.Text(), nullable=False),
        sa.Column('parent_id', sa.Text(), nullable=False),
        sa.Column('kd_prov', sa.Text(), sa.Computed("substr(id, 1, 2)")),
        sa.Column('kd_kab', sa.Text(), sa.Computed("substr(id, 3, 2)")),
        sa.Column('kd_kec', sa.Text(), sa.Computed("substr(id, 5, 3)")),
        sa.Column('kd_kel', sa.Text(), sa.Computed("substr(id, 8, 3)")),
        sa.Column('kd_rw', sa.Text(), sa.Computed("substr(id, 11, 3)")),
        sa.Column('kd_rt', sa.Text(), sa.Computed("substr(id, 14, 3)")),
        sa.Column('tag_id', sa.Text, nullable=True)
    )

    op.create_table(
        "user_regions",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("region_id", sa.Text(), sa.ForeignKey("regions.id", ondelete="CASCADE"), nullable=False)
    )

    op.create_table(
        'region_aggregates',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False, autoincrement=True),
        sa.Column('date', sa.Date, nullable=False),
        sa.Column('kec_id', sa.Text, sa.ForeignKey("regions.id",  ondelete="CASCADE"), sa.Computed("substr(rt_id, 1, 7)")),
        sa.Column('kel_id', sa.Text, sa.ForeignKey("regions.id",  ondelete="CASCADE"), sa.Computed("substr(rt_id, 1, 10)")),
        sa.Column('rw_id', sa.Text,  sa.ForeignKey("regions.id",  ondelete="CASCADE"), sa.Computed("substr(rt_id, 1, 13)")),
        sa.Column('rt_id', sa.Text,  sa.ForeignKey("regions.id",  ondelete="CASCADE"), nullable=False),
        sa.Column('total_data', sa.Integer, nullable=False)
    )

    op.create_table(
        "etl_tracker",
        sa.Column("start_processed_at", sa.DateTime(), nullable=False),
        sa.Column("end_processed_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("start_processed_at", "end_processed_at")
    )

def downgrade() -> None:
    op.drop_table('users')

    op.drop_table('regions')

    op.drop_table('user_regions')

    op.drop_table('region_aggregates')

    op.drop_table('etl_tracker')

