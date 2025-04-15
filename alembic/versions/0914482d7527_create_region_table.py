"""create region table

Revision ID: 0914482d7527
Revises: f79819302d60
Create Date: 2025-04-14 11:31:25.890198

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0914482d7527'
down_revision: Union[str, None] = 'f79819302d60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'regions',
        sa.Column('id', sa.Text(), primary_key=True, nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('level', sa.Text(), nullable=False),
        sa.Column('parent_id', sa.Text(), nullable=False),
        sa.Column('kd_prov', sa.Text(), nullable=True),
        sa.Column('kd_kab', sa.Text(), nullable=True),
        sa.Column('kd_kec', sa.Text(), nullable=True),
        sa.Column('kd_kel', sa.Text(), nullable=True),
        sa.Column('kd_rw', sa.Text(), nullable=True),
        sa.Column('kd_rt', sa.Text(), nullable=True)
    )

    op.create_index('ix_regions_id', 'regions', ['id']) 

    op.execute("""
        CREATE TRIGGER set_kd_fields_after_insert 
        AFTER INSERT ON regions
        FOR EACH ROW
        BEGIN
            UPDATE regions SET
                kd_prov = substr(NEW.id, 1, 2),
                kd_kab = substr(NEW.id, 3, 2),
                kd_kec = substr(NEW.id, 5, 3),
                kd_kel = substr(NEW.id, 8, 3),
                kd_rw  = substr(NEW.id, 11, 3),
                kd_rt  = substr(NEW.id, 14, 3)
            WHERE id = NEW.id;
        END;
    """)


def downgrade() -> None:
    op.drop_index('ix_regions_id', table_name='regions')
    op.execute("DROP TRIGGER IF EXISTS set_kd_fields_after_insert;")
    op.drop_table('regions')
