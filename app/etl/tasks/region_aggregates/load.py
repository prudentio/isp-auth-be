import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.region_aggregate import RegionAggregates
from app.models.etl_tracker import EtlTracker
from datetime import datetime

async def insert_aggregated_data(data: pd.DataFrame, db: AsyncSession):
    for _, row in data.iterrows():
        new_record = RegionAggregates(
            date=row["date"],
            rt_id=row["region_id"],
            total_data=row["total_data"]
        )

        db.add(new_record)
    
    await db.commit()

async def update_etl_tracking(start_processed_at : datetime, end_processed_at: datetime, db:AsyncSession):
    tracking = EtlTracker(
       start_processed_at = start_processed_at,
       end_processed_at = end_processed_at
    )

    db.add(tracking)
    await db.commit()