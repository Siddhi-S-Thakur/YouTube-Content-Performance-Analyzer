from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Creator Content Intelligence"
    API_V1_STR: str = "/api"
    APP_ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    # Database & Integrations (for future phases)
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/creator_intelligence"
    YOUTUBE_API_KEY: str = ""
    OPENAI_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
