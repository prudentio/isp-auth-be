from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import Users

async def verify_user(db: AsyncSession, username: str):
    result = await db.execute(select(Users).where(Users.username ==  username))

    return result.scalar_one_or_none()