from app.etl.tasks.region_aggregates.extract import extract_region_data
from app.etl.tasks.region_aggregates.transform import transform_region_data
from app.etl.tasks.region_aggregates.load import load_aggregated_region_data
from app.etl.load import update_etl_tracking
from app.infrastructure.db.session import AsyncSessionGeoform, AsyncSessionDashboard
from app.models.region_aggregate import RegionAggregates

async def run_region_aggregates_etl():
    async with AsyncSessionGeoform() as geoform_session, AsyncSessionDashboard() as dashboard_session:
        extracted_data = await extract_region_data(geoform_session, dashboard_session)

        if extracted_data:
            transformed_data = await transform_region_data(extracted_data, dashboard_session)
            await load_aggregated_region_data(transformed_data, dashboard_session, RegionAggregates)

            start_processed_data = extracted_data[0]
            start_processed_at = start_processed_data.updated_at

            end_processed_data = extracted_data[-1]
            end_processed_at = end_processed_data.updated_at
            
            await update_etl_tracking(start_processed_at, end_processed_at, dashboard_session)