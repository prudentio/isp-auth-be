from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_region import UserRegions
from sqlalchemy import select

async def get_user_regions_by_user_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(UserRegions.region_id).where(UserRegions.user_id ==  user_id))

    region_ids = result.scalars().all() 
    return region_ids
     