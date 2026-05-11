"""init auth tables

Revision ID: 9031be8c7c13
Revises: 
Create Date: 2026-05-10 16:01:58.058656

"""
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy import table, column
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '9031be8c7c13'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        'roles',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('name', sa.Text(), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        'permissions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('code', sa.Text(), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        'role_permissions',
        sa.Column('role_id', UUID(as_uuid=True), sa.ForeignKey('roles.id', ondelete='CASCADE'), nullable=False),
        sa.Column('permission_id', UUID(as_uuid=True), sa.ForeignKey('permissions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('role_id', 'permission_id')
    )

    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('username', sa.Text(), nullable=False, unique=True),
        sa.Column('password', sa.Text(), nullable=False),
        sa.Column('role_id', UUID(as_uuid=True), sa.ForeignKey('roles.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    )

    roles_table = table(
        "roles",
        column("id", UUID(as_uuid=True)),
        column("name", sa.Text),
    )

    permissions_table = table(
        "permissions",
        column("id", UUID(as_uuid=True)),
        column("code", sa.Text),
    )

    role_permissions_table = table(
        "role_permissions",
        column("role_id", UUID(as_uuid=True)),
        column("permission_id", UUID(as_uuid=True)),
    )

    users_table = table(
        "users",
        column("id", UUID(as_uuid=True)),
        column("username", sa.Text),
        column("password", sa.Text),
        column("role_id", UUID(as_uuid=True)),
    )

    admin_role_id = uuid.uuid4()

    op.execute(
        roles_table.insert().values(
            id=admin_role_id,
            name="admin"
        )
    )

    perms = [
        ("MAP", uuid.uuid4()),
        ("CONFIG", uuid.uuid4()),
        ("MAP_EDIT", uuid.uuid4()),
        ("AUDIT", uuid.uuid4()),
    ]

    for code, pid in perms:
        op.execute(
            permissions_table.insert().values(
                id=pid,
                code=code
            )
        )

    for _, pid in perms:
        op.execute(
            role_permissions_table.insert().values(
                role_id=admin_role_id,
                permission_id=pid
            )
        )

    op.execute(
        users_table.insert().values(
            id=uuid.uuid4(),
            username="prudentiofalah28@gmail.com",
            password="$argon2i$v=19$m=16,t=2,p=1$YktLblBlVUlmREo4bWZwUQ$/sGstcyn1FT91Q9T7xxudg",
            role_id=admin_role_id
        )
    )


def downgrade() -> None:
    op.drop_table('users')
    op.drop_table('role_permissions')
    op.drop_table('permissions')
    op.drop_table('roles')