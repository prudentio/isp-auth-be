from app.etl.extract import extract_data
from app.etl.load import insert_aggregated_data, update_etl_tracking, update_family_card_data
from app.etl.transform import aggregate_data, transform_data
from app.infrastructure.db.session import AsyncSessionGeoform, AsyncSessionDashboard
from app.models.region_aggregate import RegionAggregates
from app.models.surveyor_aggregate import SurveyorAggregates
from app.schemas.etl import TypeAggregateEnum

async def run_etl():
    async with AsyncSessionGeoform() as geoform_session, AsyncSessionDashboard() as dashboard_session:
        extracted_data, family_card_set = await extract_data(geoform_session, dashboard_session)

        if extracted_data:
            transformed_data = await transform_data(extracted_data, dashboard_session, geoform_session)
            
            # Aggregate Region
            aggregated_region_data = await aggregate_data(transformed_data, TypeAggregateEnum.REGION)
            await insert_aggregated_data(aggregated_region_data, dashboard_session, RegionAggregates)

            # Aggregate Surveyor
            aggregated_surveyor_data = await aggregate_data(transformed_data, TypeAggregateEnum.SURVEYOR)
            await insert_aggregated_data(aggregated_surveyor_data, dashboard_session, SurveyorAggregates)

            # Update Family Card Table
            await update_family_card_data(dashboard_session, family_card_set)

            # Update ETL Tracker Table
            start_processed_at = extracted_data[0].date
            end_processed_at   = extracted_data[-1].date
            await update_etl_tracking(start_processed_at, end_processed_at, dashboard_session)