import uuid
import datetime
from typing import List

from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role_permissions import RolePermissions
from app.models.roles import Roles
from app.models.permissions import Permissions
from app.schemas.role import CreateRoleRequest
from app.services.permission import get_permissions_by_ids

async def get_roles(db: AsyncSession) -> List[Roles]:
    stmt = (
        select(Roles)
        .where(Roles.deleted_at.is_(None))
        .options(selectinload(Roles.permissions))
    )

    result = await db.execute(stmt)
    return result.scalars().all()

async def get_role_by_id(db: AsyncSession, role_id: uuid.UUID):
    stmt = (
        select(Roles)
        .where(
            Roles.id == role_id,
            Roles.deleted_at.is_(None)
        )
        .options(selectinload(Roles.permissions))
    )

    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_role(db: AsyncSession, payload: CreateRoleRequest) -> Roles:
    role = Roles(
        id=uuid.uuid4(),
        name=payload.name,
        created_at=datetime.datetime.now()
    )

    db.add(role)
    await db.flush() 

    for pid in payload.permission_ids:
        db.add(RolePermissions(
            role_id=role.id,
            permission_id=pid
        ))

    await db.commit()

    # reload role + permissions biar return lengkap
    result = await db.execute(
        select(Roles)
        .where(Roles.id == role.id)
        .options(selectinload(Roles.permissions))
    )

    return result.scalar_one()

async def update_role_permissions(
    db: AsyncSession,
    role_id: uuid.UUID,
    permission_ids: list[uuid.UUID]
) -> Roles | None:

    result = await db.execute(
        select(Roles)
        .where(
            Roles.id == role_id,
            Roles.deleted_at.is_(None)
        )
    )

    role = result.scalar_one_or_none()

    if not role:
        return None

    perm_result = await db.execute(
        select(Permissions).where(
            Permissions.id.in_(permission_ids),
            Permissions.deleted_at.is_(None)
        )
    )

    permissions = perm_result.scalars().all()

    role.permissions = permissions
    role.updated_at = datetime.datetime.now()

    await db.commit()
    await db.refresh(role)

    return role

async def delete_role(
    db: AsyncSession,
    role_id: uuid.UUID
) -> uuid.UUID:

    now = datetime.datetime.now()

    result = await db.execute(
        select(Roles).where(Roles.id == role_id)
    )

    role = result.scalar_one_or_none()

    if not role:
        return None

    role.deleted_at = now

    await db.execute(
        update(RolePermissions)
        .where(RolePermissions.role_id == role_id)
        .values(deleted_at=now)
    )

    await db.commit()

    return role.id