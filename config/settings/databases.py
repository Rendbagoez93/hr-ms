"""
Database configuration for different environments.
SQLite for development, PostgreSQL for production.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(ABC):
    """Abstract base class for database configuration."""

    @abstractmethod
    def get_config(self) -> dict[str, Any]:
        pass


class SQLiteConfig(BaseSettings, DatabaseConfig):
    """SQLite database configuration for development."""

    model_config = SettingsConfigDict(
        env_prefix="SQLITE_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    db_name: str = Field(
        default="db.sqlite3",
        description="SQLite database filename",
    )

    base_dir: Path = Field(
        default_factory=lambda: Path(__file__).resolve().parent.parent.parent,
        description="Base directory for database file",
    )

    @property
    def db_path(self) -> Path:
        """Get full database path."""
        return self.base_dir / self.db_name

    def get_config(self) -> dict[str, Any]:
        """Get SQLite database configuration."""
        return {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": str(self.db_path),
                "ATOMIC_REQUESTS": True,
            }
        }


class PostgreSQLConfig(BaseSettings, DatabaseConfig):
    """PostgreSQL database configuration for production."""

    model_config = SettingsConfigDict(
        env_prefix="POSTGRES_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    host: str = Field(
        default="localhost",
        description="PostgreSQL host",
    )

    port: int = Field(
        default=5432,
        description="PostgreSQL port",
    )

    user: str = Field(
        ...,
        description="PostgreSQL user",
    )

    password: str = Field(
        ...,
        description="PostgreSQL password",
    )

    db: str = Field(
        ...,
        description="PostgreSQL database name",
    )

    schema: str = Field(
        default="public",
        description="PostgreSQL schema",
    )

    conn_max_age: int = Field(
        default=600,
        description="Connection max age in seconds",
    )

    pool_size: int = Field(
        default=20,
        description="Connection pool size",
    )

    ssl_mode: str = Field(
        default="require",
        description="SSL mode for connection",
    )

    @field_validator("port")
    @classmethod
    def validate_port(cls, v: int) -> int:
        """Validate PostgreSQL port."""
        if not 1 <= v <= 65535:
            raise ValueError("Port must be between 1 and 65535")
        return v

    @property
    def connection_url(self) -> str:
        """Get PostgreSQL connection URL."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    def get_config(self) -> dict[str, Any]:
        """Get PostgreSQL database configuration."""
        return {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": self.db,
                "USER": self.user,
                "PASSWORD": self.password,
                "HOST": self.host,
                "PORT": self.port,
            }
        }


class DatabaseFactory:
    """Factory class for creating database configurations."""

    @staticmethod
    def create(environment: str) -> DatabaseConfig:
        environment = environment.lower()

        if environment == "development":
            return SQLiteConfig()
        elif environment == "production":
            return PostgreSQLConfig()
        else:
            raise ValueError(
                f"Unsupported environment: {environment}. "
                "Must be 'development' or 'production'."
            )

    @staticmethod
    def get_databases_config(environment: str) -> dict[str, Any]:
        db_config = DatabaseFactory.create(environment)
        return db_config.get_config()
