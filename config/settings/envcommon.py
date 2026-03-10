from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    SECRET_KEY: str
    DEBUG: bool = Field(default=False)
    ENVIRONMENT: str = Field(default="local")
    ALLOWED_HOSTS: list[str] = Field(default=["localhost", "127.0.0.1"])
    LANGUAGE_CODE: str = Field(default="en-us")
    CORS_ALLOWED_ORIGINS: list[str] = Field(default=[])
    CELERY_BROKER_URL: str = Field(default="redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = Field(default="redis://localhost:6379/0")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )
