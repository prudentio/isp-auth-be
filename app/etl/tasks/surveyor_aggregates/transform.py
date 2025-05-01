from typing import List, Tuple
from datetime import datetime
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.etl.transform import aggregate_data, transform_data

async def transform_surveyor_data(
        data: List[Tuple[datetime, List[UUID], UUID]], 
        db_dashboard: AsyncSession, 
        db_geoform: AsyncSession):
    
    transformed_data = await transform_data(data, db_dashboard, db_geoform)

    group_columns =  ['date', 'region_id', 'surveyor_id','surveyor_name']
    grouped_data = await aggregate_data(transformed_data,group_columns)

    return grouped_data