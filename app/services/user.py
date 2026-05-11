import uuid
import datetime
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.security import hash_pw
from app.models.roles import Roles
from app.models.user import Users
from sqlalchemy.orm import selectinload

async def get_users(db: AsyncSession):
    stmt = (
        select(Users)
        .where(Users.deleted_at.is_(None))
        .options(
            selectinload(Users.role)
            .selectinload(Roles.permissions),
        )
    )

    result = await db.execute(stmt)
    return result.scalars().all()

async def get_user_by_id(
    db: AsyncSession,
    user_id: uuid.UUID
) -> Users:

    stmt = select(Users).where(
        Users.id == user_id,
        Users.deleted_at.is_(None)
    ).options(
            selectinload(Users.role)
            .selectinload(Roles.permissions),
        )

    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_role_by_id(db: AsyncSession, role_id: uuid.UUID):
    result = await db.execute(
        select(Roles).where(
            Roles.id == role_id,
            Roles.deleted_at.is_(None)
        )
    )

    return result.scalar_one_or_none()


async def create_user(
    db: AsyncSession,
    username: str,
    password: str,
    role_id: uuid.UUID,
) -> Users:
    user = Users(
        username=username,
        password=hash_pw(password),
        role_id=role_id,
        created_at=datetime.datetime.now()
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def update_user(
    db: AsyncSession,
    user_id: uuid.UUID,
    username: str | None,
    password: str | None,
    role_id: uuid.UUID | None,
):

    stmt = (
        update(Users)
        .where(
            Users.id == user_id,
            Users.deleted_at.is_(None)
        )
        .values(
            **{
                k: v for k, v in {
                    "username": username,
                    "password": password,
                    "role_id": role_id,
                    "updated_at": datetime.datetime.now()
                }.items()
                if v is not None
            }
        )
    )

    await db.execute(stmt)
    await db.commit()

    return True
async def delete_user(
    db: AsyncSession,
    user_id: uuid.UUID
) -> bool:

    stmt = (
        update(Users)
        .where(
            Users.id == user_id,
            Users.deleted_at.is_(None)
        )
        .values(
            deleted_at=datetime.datetime.now()
        )
    )

    result = await db.execute(stmt)
    await db.commit()

    return result.rowcount > 0