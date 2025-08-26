from datetime import datetime
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.etl_tracker import EtlTracker
from datetime import timezone
from app.models.family_card import FamilyCards
from app.models.geoform.project_data import ProjectData
from app.schemas.etl import ExtractedData
from app.schemas.geoform.project_data import ProjectDataDict
from sqlalchemy.dialects.postgresql import JSONB

PROJECT_KEY = "hzxslWgU2q"
FAMILY_CARD_KEY = "zb7nDHAJgi"

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

async def extract_existing_family_card(db_dashboard:AsyncSession):
    results = await db_dashboard.execute(select(FamilyCards.id))
    family_card_set = {row[0] for row in results}
    
    return family_card_set

async def extract_family_card_survey_data(pd_data: ProjectDataDict):
    json_data = pd_data.get(PROJECT_KEY, [])

    if not isinstance(json_data, list) or not json_data:
        return []  

    fc_values = [row.get(FAMILY_CARD_KEY) for row in json_data if row.get(FAMILY_CARD_KEY)]
    fc_values = list(set(fc_values))

    return fc_values

async def extract_data(db_geoform:AsyncSession, db_dashboard: AsyncSession):
    last_processed_at = await get_last_processed_at(db_dashboard)

    result = await db_geoform.execute(
        select(ProjectData.data, ProjectData.created_at, ProjectData.tag_id, ProjectData.created_by)
        .where(ProjectData.created_at > last_processed_at)
        )

    rows = result.all()
    
    family_card_set = await extract_existing_family_card(db_dashboard)

    processed: List[ExtractedData] = []

    for pd_data, pd_created_at, pd_tag, pd_created_by in rows:
        # 1. Get Family Card From Survey
        fc_values = await extract_family_card_survey_data(pd_data)

        # 2. Filter out family card numbers that are not in the hash set
        new_kk_values = [kk for kk in fc_values if kk not in family_card_set]

        if new_kk_values:
            family_card_set.update(new_kk_values)

            processed.append(
                ExtractedData(
                    date=pd_created_at,
                    tag_id=pd_tag,
                    surveyor_id=pd_created_by,
                    family_cards=new_kk_values
                )
            )

    return processed, family_card_set

