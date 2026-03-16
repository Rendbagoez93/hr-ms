import os
from enum import StrEnum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, field_validator
from pydantic_core import PydanticCustomError
from pydantic_settings import BaseSettings, SettingsConfigDict


_BASE_DIR = Path(__file__).resolve().parent.parent.parent


class DBEngineEnum(StrEnum):
    SQLITE = "django.db.backends.sqlite3"
    POSTGRES = "django.db.backends.postgresql"


class BaseDatabaseSettings(BaseSettings):
    engine: DBEngineEnum = DBEngineEnum.SQLITE

    model_config = SettingsConfigDict(
        env_prefix="DATABASE_",
        extra="ignore",
        frozen=True,
        alias_generator=lambda field_name: field_name.upper(),
        populate_by_name=True,
        env_file=".env",
    )

    @field_validator("engine", mode="before")
    @classmethod
    def validate_engine(cls, v: Any) -> DBEngineEnum:
        if isinstance(v, DBEngineEnum):
            return v
        if isinstance(v, str):
            try:
                return DBEngineEnum[v.upper()]
            except KeyError:
                pass
            for member in DBEngineEnum:
                if v == member.value:
                    return member
        valid_names = [m.name for m in DBEngineEnum]
        valid_values = [m.value for m in DBEngineEnum]
        raise PydanticCustomError(
            "enum",
            f"Input should be one of {valid_names} or {valid_values}",
            {"input": v, "valid_names": valid_names, "valid_values": valid_values},
        )


class SqliteDatabaseSettings(BaseDatabaseSettings):
    engine: DBEngineEnum = DBEngineEnum.SQLITE
    name: str = str(_BASE_DIR / "db.sqlite3")

    @field_validator("name", mode="before")
    @classmethod
    def resolve_sqlite_path(cls, v: Any) -> str:
        s = str(v)
        # A bare name (no path separators) is a Postgres-style DB name, not a file path.
        # Fall back to the default SQLite file location in BASE_DIR.
        if os.sep not in s and "/" not in s:
            return str(_BASE_DIR / "db.sqlite3")
        path = Path(s)
        return s if path.is_absolute() else str(_BASE_DIR / path)


class PostgresDatabaseSettings(BaseDatabaseSettings):
    engine: DBEngineEnum = DBEngineEnum.POSTGRES
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = "postgres"  # noqa: S105
    name: str = "hr_ms"


class DjangoDatabases(BaseModel):
    default: PostgresDatabaseSettings | SqliteDatabaseSettings
