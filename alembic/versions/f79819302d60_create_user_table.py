"""create_user_table

Revision ID: f79819302d60
Revises: 
Create Date: 2025-04-10 10:31:08.471807

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f79819302d60'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('username', sa.Text(), nullable=False, unique=True),
        sa.Column('password', sa.Text(), nullable=False),
    )
    op.create_index('ix_users_id', 'users', ['id']) 

    op.execute(""" 
        INSERT INTO users (id, username, password) 
        VALUES (
            1, 
            'admin', 
            '$argon2i$v=19$m=16,t=2,p=1$UU5tWVFZZ1ZFVHFCV1R1bw$3neLY/prgGXzYeIZK5InDw'
        ) 
    """)

def downgrade() -> None:
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')