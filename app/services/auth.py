from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.roles import Roles
from app.models.user import Users

async def verify_user(db: AsyncSession, username: str):
    result = await db.execute(
        select(Users)
        .options(
            selectinload(Users.role)
            .selectinload(Roles.permissions),
        )
        .where(Users.username == username)
    )

    return result.scalar_one_or_none()