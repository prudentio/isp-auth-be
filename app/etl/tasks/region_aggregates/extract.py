from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.geoform.project_data import ProjectData
from dateutil.parser import parse
from app.models.etl_tracker import EtlTracker
from datetime import timezone

async def get_last_processed_at(dbDashboard: AsyncSession):
    result = await dbDashboard.execute(
        select(EtlTracker.end_processed_at)
        .order_by(EtlTracker.end_processed_at.desc())
        .limit(1)
    )

    last_processed_etl = result.scalar_one_or_none()
    last_processed_at = last_processed_etl if last_processed_etl else datetime.min

    return last_processed_at

async def extract_tag_id(dbGeoform:AsyncSession, dbDashboard: AsyncSession):
    last_processed_at = await get_last_processed_at(dbDashboard)

    if last_processed_at.tzinfo is None:
        last_processed_at = last_processed_at.replace(tzinfo=timezone.utc)
    else:
        last_processed_at = last_processed_at.astimezone(timezone.utc)

    result = await dbGeoform.execute(
        select(ProjectData.updated_at, ProjectData.tag_id)
        .where(ProjectData.updated_at > last_processed_at)
        )

    rows = result.all()
    return rows