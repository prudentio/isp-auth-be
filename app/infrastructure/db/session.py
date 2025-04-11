from app.infrastructure.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator

DATABASE_URL = settings.DATABASE_URL
RUN_MODE = settings.RUN_MODE

engine = create_async_engine(
            DATABASE_URL, 
            echo= RUN_MODE == "DEVELOPMENT"
        )

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session