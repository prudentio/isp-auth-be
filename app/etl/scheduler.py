import asyncio
from aiojobs import create_scheduler
from app.etl.tasks.region_aggregates.etl_runner import run_region_aggregates_etl
from app.etl.tasks.surveyor_aggregates.etl_runner import run_surveyor_aggregates_etl
from app.infrastructure.config import settings
from app.infrastructure.db.session import engine_geoform, engine_dashboard
import aiohttp
from datetime import datetime, timedelta

class EtlJob:
    def __init__(self, hour: int = settings.ETL_SCHEDULE_HOUR):
        self.hour = hour
        self.scheduler = None
        self.session : aiohttp.ClientSession | None = None
    
    async def start(self):
        self.scheduler = await create_scheduler()
        self.session = aiohttp.ClientSession()

        await self.scheduler.spawn(self._repeat_etl())
    
    async def stop(self):
        await self.cleanup()

    async def cleanup(self):
        await self.shutdown_db_connection()
        await self.shutdown_http_connection()
        await self.shutdown_scheduler()

    async def shutdown_scheduler(self):
        if self.scheduler:
            await self.scheduler.close()
    
    async def shutdown_http_connection(self):
        if self.session:
            try:
                await self.session.close()
            except Exception as e:
                raise RuntimeError("Failed to close the HTTP connection") from e

    async def shutdown_db_connection(self):
        await self.shutdown_postgresql_connection()
        await self.shutdown_sqlite_connection()

    async def shutdown_postgresql_connection(self):
        try:
            await engine_geoform.dispose()
        except Exception as e:
            raise RuntimeError("Failed to close the PostgreSQL connection") from e
    
    async def shutdown_sqlite_connection(self):
        try:
            await engine_dashboard.dispose()
        except Exception as e:
            raise RuntimeError("Failed to close the SQLite connection") from e
        
    async def _repeat_etl(self):
        while True:
            now = datetime.now()
            next_run = now.replace(hour=self.hour, minute=0, second=0, microsecond=0)

            if now > next_run:
                next_run += timedelta(days=1)

            delay = (next_run - now).total_seconds()
            await asyncio.sleep(delay)
            await run_surveyor_aggregates_etl()
            await run_region_aggregates_etl()
