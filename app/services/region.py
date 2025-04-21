from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.region import Regions
from app.schemas.region import GetRegionByLevelResponse, RegionLevel

async def get_region_by_level(db: AsyncSession, level: RegionLevel):
    result = await db.execute(
        select(Regions.id, Regions.name, Regions.parent_id).where(Regions.level == level)
    )
    rows = result.all()

    return [
        GetRegionByLevelResponse(
            id=region_id,
            name=name,
            parent_id=parent_id
        )
        for region_id, name, parent_id in rows
    ]
