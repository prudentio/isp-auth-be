from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    PORT: int = 8080
    SECRET_KEY: str
    ALGORITHM: str = "HS256" 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 
    ALLOWED_ORIGINS: List[str] = ["*"]
    RUN_MODE: str = "PRODUCTION"

    class Config:
        env_file = ".env"

settings = Settings()
