from app.etl.tasks.surveyor_aggregates.extract import extract_surveyor_data
from app.etl.tasks.surveyor_aggregates.transform import transform_surveyor_data
from app.etl.tasks.surveyor_aggregates.load import load_aggregated_surveyor_data
from app.infrastructure.db.session import AsyncSessionGeoform, AsyncSessionDashboard
from app.models.surveyor_aggregate import SurveyorAggregates

async def run_surveyor_aggregates_etl():
    async with AsyncSessionGeoform() as geoform_session, AsyncSessionDashboard() as dashboard_session:
        extracted_data = await extract_surveyor_data(geoform_session, dashboard_session)

        if extracted_data:
            transformed_data = await transform_surveyor_data(extracted_data, dashboard_session, geoform_session)
            await load_aggregated_surveyor_data(transformed_data, dashboard_session, SurveyorAggregates)