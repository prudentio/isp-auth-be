from app.infrastructure.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator

def create_session(database_url: str, echo: bool) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(database_url, echo=echo)
    return engine, async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

# Load DB
engine_dashboard, AsyncSessionDashboard = create_session(settings.DATABASE_DASHBOARD_URL, settings.RUN_MODE == "DEVELOPMENT")

async def get_db_dashboard() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionDashboard() as session:
        yield session

# Extract DB
engine_geoform, AsyncSessionGeoform = create_session(settings.DATABASE_GEOFORM_URL, settings.RUN_MODE == "DEVELOPMENT")

async def get_db_geoform() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionGeoform() as session:
        yield session