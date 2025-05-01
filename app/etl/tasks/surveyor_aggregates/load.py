import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from app.etl.load import insert_aggregated_data

async def load_aggregated_surveyor_data(data: pd.DataFrame, db_dashboard: AsyncSession, model_class):
    await insert_aggregated_data(data, db_dashboard, model_class)