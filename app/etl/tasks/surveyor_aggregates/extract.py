from sqlalchemy.ext.asyncio import AsyncSession
from app.etl.extract import get_last_processed_at
from sqlalchemy import select
from app.models.geoform.project_data import ProjectData

async def extract_surveyor_data(db_geoform:AsyncSession, db_dashboard: AsyncSession):
    last_extracted_at = await get_last_processed_at(db_dashboard)

    result = await db_geoform.execute(
        select(ProjectData.updated_at, ProjectData.tag_id,ProjectData.created_by)
        .where(ProjectData.updated_at > last_extracted_at)
        
    )

    rows = result.all()

    return rows
    
