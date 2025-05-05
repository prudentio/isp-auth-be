from typing import List
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    DATABASE_DASHBOARD_URL: str
    DATABASE_GEOFORM_URL: str
    PORT: int = 8080
    SECRET_KEY: str
    ALGORITHM: str = "HS256" 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 
    ALLOWED_ORIGINS: List[str] = ["*"]
    RUN_MODE: str = "PRODUCTION"
    ETL_SCHEDULE_HOUR: int = 2
    EXCEL_EXPORTS_DIR_PATH : Path

    class Config:
        env_file = ".env"

settings = Settings()