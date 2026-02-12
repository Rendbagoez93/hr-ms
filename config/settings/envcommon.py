"""
Environment-specific configuration using Pydantic Settings.
Supports development and production environments.
"""

from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    """Supported environment types."""

    DEVELOPMENT = "development"
    PRODUCTION = "production"


class CommonSettings(BaseSettings):
    """Common settings shared across all environments."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Environment
    environment: Environment = Field(
        default=Environment.DEVELOPMENT,
        description="Current environment (development or production)",
    )

    # Security
    secret_key: str = Field(
        default="django-insecure-change-me-in-production",
        description="Django secret key",
    )

    debug: bool = Field(
        default=True,
        description="Enable debug mode",
    )

    allowed_hosts: list[str] = Field(
        default_factory=lambda: ["localhost", "127.0.0.1"],
        description="Allowed hosts for the application",
    )

    # Application
    base_dir: Path = Field(
        default_factory=lambda: Path(__file__).resolve().parent.parent.parent,
        description="Base directory of the project",
    )

    # CORS
    cors_allowed_origins: list[str] = Field(
        default_factory=list,
        description="CORS allowed origins",
    )

    # Time & Locale
    language_code: str = Field(
        default="en-us",
        description="Language code",
    )

    time_zone: str = Field(
        default="Asia/Jakarta",
        description="Time zone",
    )

    use_i18n: bool = Field(
        default=True,
        description="Enable internationalization",
    )

    use_tz: bool = Field(
        default=True,
        description="Enable timezone support",
    )

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: str, info: Any) -> str:
        """Validate secret key in production."""
        environment = info.data.get("environment")
        if environment == Environment.PRODUCTION and "insecure" in v:
            raise ValueError("Secret key must be changed in production")
        return v

    @field_validator("debug")
    @classmethod
    def validate_debug(cls, v: bool, info: Any) -> bool:
        """Ensure debug is disabled in production."""
        environment = info.data.get("environment")
        if environment == Environment.PRODUCTION and v is True:
            return False
        return v

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment == Environment.DEVELOPMENT

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment == Environment.PRODUCTION


class DevelopmentSettings(CommonSettings):
    """Development-specific settings."""

    environment: Environment = Field(default=Environment.DEVELOPMENT)
    debug: bool = Field(default=True)
    allowed_hosts: list[str] = Field(
        default_factory=lambda: ["localhost", "127.0.0.1", "*"]
    )


class ProductionSettings(CommonSettings):
    """Production-specific settings."""

    environment: Environment = Field(default=Environment.PRODUCTION)
    debug: bool = Field(default=False)
    secret_key: str = Field(
        ...,
        description="Django secret key (must be set via environment variable)",
    )
    allowed_hosts: list[str] = Field(
        ...,
        description="Allowed hosts (must be set via environment variable)",
    )


def get_settings() -> CommonSettings:

    env = Environment(
        CommonSettings()
        .model_config.get("env_file", ".env")
        and CommonSettings().environment
        or Environment.DEVELOPMENT
    )

    if env == Environment.PRODUCTION:
        return ProductionSettings()
    return DevelopmentSettings()
