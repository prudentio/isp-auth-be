from typing import List, Optional, Tuple
from datetime import datetime, date
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.region import Regions
from sqlalchemy import select
import pandas as pd
from app.models.geoform.user_account import UserAccount

async def transform_date(updated_at: datetime):
    transformed_date = updated_at.date()
    return transformed_date

async def transform_tag_id(tag_ids: List[UUID], db_dashboard: AsyncSession):
    tag_id = str(tag_ids[0])
    result = await db_dashboard.execute(select(Regions.id).where(Regions.tag_id == tag_id))
    region_id = result.scalar_one_or_none()

    return region_id

async def transform_surveyor_id(surveyor_id: str, db_geoform: AsyncSession):
    result = await db_geoform.execute(
                select(UserAccount.username)
                .where(UserAccount.id == surveyor_id)
            )

    surveyor_name = result.scalar_one_or_none()
    return surveyor_name

async def transform_data(
        data: List[Tuple[datetime, List[UUID], Optional[UUID]]], 
        db_dashboard: AsyncSession, 
        db_geoform: Optional[AsyncSession] = None
        ):
    transformed_data = []

    for entry in data:
        #Transform Date
        updated_at = entry[0]
        transformed_date = await transform_date(updated_at)

        #Transform Tag Id
        tag_ids = entry[1]
        region_id = await transform_tag_id(tag_ids, db_dashboard)

        #Transform Surveyor Id
        surveyor_id = entry[2] if len(entry)> 2 else None
        if surveyor_id:
            surveyor_name = await transform_surveyor_id(surveyor_id, db_geoform)
            transformed_data.append((transformed_date, region_id, str(surveyor_id), surveyor_name))
        else:
            transformed_data.append((transformed_date, region_id))

    return transformed_data

async def aggregate_data(
        data: List[Tuple[date, str, Optional[str], Optional[str]]], 
        group_columns: List[str]
    ):
    df = pd.DataFrame(data, columns = group_columns)
    grouped = df.groupby(group_columns).size().reset_index(name='total_data')

    return grouped