from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.etl_tracker import EtlTracker
from datetime import timezone

async def get_last_processed_at(db_dashboard: AsyncSession):
    result = await db_dashboard.execute(
        select(EtlTracker.end_processed_at)
        .order_by(EtlTracker.end_processed_at.desc())
        .limit(1)
    )

    last_processed_etl = result.scalar_one_or_none()
    last_processed_at = last_processed_etl if last_processed_etl else datetime.min

    if last_processed_at.tzinfo is None:
        last_processed_at = last_processed_at.replace(tzinfo=timezone.utc)
    else:
        last_processed_at = last_processed_at.astimezone(timezone.utc)

    return last_processed_at
