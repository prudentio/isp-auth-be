from typing import List, Tuple
from datetime import datetime, date
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.region import Regions
from sqlalchemy import select
import pandas as pd

async def convert_to_region_id_data(data: List[Tuple[datetime, List[UUID]]], db: AsyncSession):
    converted_data = []

    for updated_at, tags_id in data:
        transformed_date = updated_at.date()

        tag_id = str(tags_id[0]) 
        result = await db.execute(select(Regions.id).where(Regions.tag_id == tag_id))
        region_id = result.scalar_one_or_none()

        converted_data.append((transformed_date, region_id))

    return converted_data

async def aggregate_region_id(data: List[Tuple[date, str]]):
    df = pd.DataFrame(data, columns=['date', 'region_id'])
    grouped = df.groupby(['date', 'region_id']).size().reset_index(name='total_data')

    return grouped

async def transform_tag_id(data: List[Tuple[datetime, List[UUID]]], db: AsyncSession):    
    converted_data = await convert_to_region_id_data(data, db)
    grouped_data = await aggregate_region_id(converted_data)

    return grouped_data    