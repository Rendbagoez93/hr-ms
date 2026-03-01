from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    SECRET_KEY: str = Field(default="django-insecure-change-this-in-production")
    DEBUG: bool = Field(default=False)
    ENVIRONMENT: str = Field(default="local")
    ALLOWED_HOSTS: list[str] = Field(default=["localhost", "127.0.0.1"])
    LANGUAGE_CODE: str = Field(default="en-us")
    CORS_ALLOWED_ORIGINS: list[str] = Field(default=[])

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )
