from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.geoform.project_data import ProjectData
from app.etl.extract import get_last_processed_at

async def extract_region_data(db_geoform:AsyncSession, db_dashboard: AsyncSession):
    last_processed_at = await get_last_processed_at(db_dashboard)

    result = await db_geoform.execute(
        select(ProjectData.updated_at, ProjectData.tag_id)
        .where(ProjectData.updated_at > last_processed_at)
        )

    rows = result.all()
    return rows