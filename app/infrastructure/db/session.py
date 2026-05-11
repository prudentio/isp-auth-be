from app.infrastructure.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator

def create_session(database_url: str, echo: bool) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(database_url, echo=echo)
    return engine, async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

# Extract DB
engine_db, AsyncSessionDb = create_session(settings.DATABASE_URL, settings.RUN_MODE == "DEVELOPMENT")

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionDb() as session:
        yield session