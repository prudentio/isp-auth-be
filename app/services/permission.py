import uuid
import datetime
from typing import List
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.permissions import Permissions
from app.schemas.permission import CreatePermissionRequest, UpdatePermissionRequest

async def get_many_permissions(db: AsyncSession) -> List[Permissions]:
    stmt = select(Permissions).where(
        Permissions.deleted_at.is_(None)
    )

    result = await db.execute(stmt)
    return result.scalars().all()

async def get_permissions_by_ids(
    db: AsyncSession,
    ids: list[uuid.UUID]
) -> list[Permissions]:

    stmt = select(Permissions).where(
        Permissions.id.in_(ids),
        Permissions.deleted_at.is_(None)
    )

    result = await db.execute(stmt)
    return result.scalars().all()

async def create_permission(
    db: AsyncSession,
    payload: CreatePermissionRequest
) -> Permissions:

    new_permission = Permissions(
        code=payload.code,
        created_at=datetime.datetime.now()
    )

    db.add(new_permission)
    await db.commit()
    await db.refresh(new_permission)

    return new_permission


async def update_permission(
    db: AsyncSession,
    permission_id: uuid.UUID,
    payload: UpdatePermissionRequest
) -> Permissions | None:

    stmt = (
        update(Permissions)
        .where(
            Permissions.id == permission_id,
            Permissions.deleted_at.is_(None)
        )
        .values(
            **{
                k: v for k, v in payload.model_dump().items()
                if v is not None
            },
            updated_at=datetime.datetime.now()
        )
        .returning(Permissions)
    )

    result = await db.execute(stmt)
    await db.commit()

    return result.scalar_one_or_none()

async def delete_permission(
    db: AsyncSession,
    permission_id: uuid.UUID
) -> uuid.UUID | None:

    stmt = (
        update(Permissions)
        .where(
            Permissions.id == permission_id,
            Permissions.deleted_at.is_(None)
        )
        .values(
            deleted_at=datetime.datetime.now()
        )
        .returning(Permissions.id)
    )

    result = await db.execute(stmt)
    await db.commit()

    return result.scalar_one_or_none()