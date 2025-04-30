from app.etl.tasks.region_aggregates.extract import extract_tag_id
from app.etl.tasks.region_aggregates.transform import transform_tag_id
from app.etl.tasks.region_aggregates.load import insert_aggregated_data, update_etl_tracking
from app.infrastructure.db.session import AsyncSessionGeoform, AsyncSessionDashboard
import pytz

utc = pytz.UTC
indonesia_timezone = pytz.timezone('Asia/Jakarta')

async def run_etl():
    async with AsyncSessionGeoform() as geoform_session, AsyncSessionDashboard() as dashboard_session:
        extracted_data = await extract_tag_id(geoform_session, dashboard_session)

        if extracted_data:
            transformed_data = await transform_tag_id(extracted_data, dashboard_session)
            await insert_aggregated_data(transformed_data, dashboard_session)

            start_processed_data = extracted_data[0]
            start_processed_at = start_processed_data.updated_at

            end_processed_data = extracted_data[-1]
            end_processed_at = end_processed_data.updated_at
            
            await update_etl_tracking(start_processed_at, end_processed_at, dashboard_session)