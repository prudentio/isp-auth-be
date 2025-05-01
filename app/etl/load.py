import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.etl_tracker import EtlTracker
from datetime import datetime

async def insert_aggregated_data(data: pd.DataFrame, db_dashboard: AsyncSession, model_class):
    for _, row in data.iterrows():
        new_record = {
            "date": row["date"],
            "rt_id": row["region_id"],
            "total_data": row["total_data"]
        }

        if "surveyor_id" in data.columns:
            new_record["surveyor_id"]  = row["surveyor_id"]
        
        if "surveyor_name" in data.columns:
            new_record["surveyor_name"] =  row["surveyor_name"]

        new_record = model_class(**new_record)  
        db_dashboard.add(new_record)
    
    await db_dashboard.commit()

async def update_etl_tracking(start_processed_at : datetime, end_processed_at: datetime, db:AsyncSession):
    tracking = EtlTracker(
       start_processed_at = start_processed_at,
       end_processed_at = end_processed_at
    )

    db.add(tracking)
    await db.commit()