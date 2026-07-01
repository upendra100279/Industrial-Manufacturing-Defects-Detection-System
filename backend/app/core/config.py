"""
Centralized application configuration loaded from environment variables.
Using pydantic-settings ensures type validation and a single source of truth.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "Industrial Defect Detection System"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    SECRET_KEY: str = "dev_secret_key_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DATABASE_URL: str = "sqlite:///./storage/defect_detection.db"

    YOLO_WEIGHTS_PATH: str = "storage/weights/best.pt"
    CONFIDENCE_THRESHOLD: float = 0.4

    ALLOWED_ORIGINS: str = "http://localhost:3000"

    class Config:
        env_file = ".env"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
