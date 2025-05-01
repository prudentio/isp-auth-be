from typing import List, Tuple
from datetime import datetime, date
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.etl.transform import transform_data, aggregate_data

async def transform_region_data(data: List[Tuple[datetime, List[UUID]]], db_dashboard: AsyncSession):    
    transformed_data = await transform_data(data, db_dashboard)

    group_columns = ['date', 'region_id']
    grouped_data = await aggregate_data(transformed_data, group_columns)

    return grouped_data    