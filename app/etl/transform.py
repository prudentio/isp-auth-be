from dataclasses import asdict, dataclass
from typing import List, Optional, Tuple
from datetime import datetime, date
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.region import Regions
from sqlalchemy import select
import pandas as pd
from app.models.geoform.user_account import UserAccount
from app.schemas.etl import AggregatedData, ExtractedData, TypeAggregateEnum

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

async def transform_total_family_card(family_cards:List[str]):
    return len(family_cards)

async def transform_data(
        data: List[ExtractedData], 
        db_dashboard: AsyncSession, 
        db_geoform: AsyncSession
        ):
    transformed_data: List[AggregatedData] = []

    for entry in data:
        # Transform Date
        transformed_date = await transform_date(entry.date)

        # Transform Tag Id
        region_id = await transform_tag_id(entry.tag_id, db_dashboard)

        # Transform Surveyor Id
        surveyor_id = entry.surveyor_id
        surveyor_name = await transform_surveyor_id(surveyor_id, db_geoform)

        # Transform Total Family Card
        total_fc = await transform_total_family_card(entry.family_cards)

        transformed_data.append(
            AggregatedData(
                date=transformed_date,
                region_id=region_id,
                surveyor_id=str(surveyor_id),
                surveyor_name=surveyor_name,
                total_data=total_fc
            )
        )

    return transformed_data

list_column_names = {
    TypeAggregateEnum.REGION: ['date', 'region_id'], 
    TypeAggregateEnum.SURVEYOR: ['date', 'region_id', 'surveyor_id','surveyor_name']
}



async def aggregate_data(
        data: List[AggregatedData], 
        type_aggregate: TypeAggregateEnum
    ) -> pd.DataFrame:
    group_columns = list_column_names[type_aggregate]
    
    if not data:
        return pd.DataFrame(columns=group_columns + ['total_data'])
    
    df = pd.DataFrame([asdict(d) for d in data])
    grouped = df.groupby(group_columns, as_index=False)['total_data'].sum()
    
    return grouped