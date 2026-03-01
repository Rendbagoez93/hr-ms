import pytest
from pydantic import ValidationError
from pydantic_core import PydanticCustomError

from config.settings.databases import (
    BaseDatabaseSettings,
    DBEngineEnum,
    DjangoDatabases,
    PostgresDatabaseSettings,
    SqliteDatabaseSettings,
)


pytestmark = pytest.mark.unit


# ─── DBEngineEnum ─────────────────────────────────────────────────────────────

def test_sqlite_enum_value():
    assert DBEngineEnum.SQLITE == "django.db.backends.sqlite3"


def test_postgres_enum_value():
    assert DBEngineEnum.POSTGRES == "django.db.backends.postgresql"


# ─── BaseDatabaseSettings.validate_engine ─────────────────────────────────────

def test_validate_engine_accepts_sqlite_name(monkeypatch):
    monkeypatch.setenv("DATABASE_ENGINE", "SQLITE")
    settings = BaseDatabaseSettings()
    assert settings.engine == DBEngineEnum.SQLITE


def test_validate_engine_accepts_postgres_name(monkeypatch):
    monkeypatch.setenv("DATABASE_ENGINE", "POSTGRES")
    settings = BaseDatabaseSettings()
    assert settings.engine == DBEngineEnum.POSTGRES


def test_validate_engine_accepts_full_sqlite_value(monkeypatch):
    monkeypatch.setenv("DATABASE_ENGINE", "django.db.backends.sqlite3")
    settings = BaseDatabaseSettings()
    assert settings.engine == DBEngineEnum.SQLITE


def test_validate_engine_accepts_full_postgres_value(monkeypatch):
    monkeypatch.setenv("DATABASE_ENGINE", "django.db.backends.postgresql")
    settings = BaseDatabaseSettings()
    assert settings.engine == DBEngineEnum.POSTGRES


def test_validate_engine_raises_on_unknown_value(monkeypatch):
    monkeypatch.setenv("DATABASE_ENGINE", "mysql")
    with pytest.raises((ValueError, PydanticCustomError)):
        BaseDatabaseSettings()


def test_base_settings_defaults_to_sqlite(monkeypatch):
    monkeypatch.delenv("DATABASE_ENGINE", raising=False)
    settings = BaseDatabaseSettings()
    assert settings.engine == DBEngineEnum.SQLITE


# ─── SqliteDatabaseSettings ───────────────────────────────────────────────────

def test_sqlite_settings_default_engine(monkeypatch):
    monkeypatch.delenv("DATABASE_ENGINE", raising=False)
    settings = SqliteDatabaseSettings()
    assert settings.engine == DBEngineEnum.SQLITE


def test_sqlite_settings_default_name_ends_with_db_sqlite3(monkeypatch):
    monkeypatch.delenv("DATABASE_NAME", raising=False)
    settings = SqliteDatabaseSettings()
    assert settings.name.endswith("db.sqlite3")


# ─── PostgresDatabaseSettings ─────────────────────────────────────────────────

def test_postgres_settings_default_host(monkeypatch):
    monkeypatch.setenv("DATABASE_ENGINE", "POSTGRES")
    monkeypatch.delenv("DATABASE_HOST", raising=False)
    settings = PostgresDatabaseSettings()
    assert settings.host == "localhost"


def test_postgres_settings_default_port(monkeypatch):
    monkeypatch.setenv("DATABASE_ENGINE", "POSTGRES")
    monkeypatch.delenv("DATABASE_PORT", raising=False)
    settings = PostgresDatabaseSettings()
    assert settings.port == 5432


def test_postgres_settings_default_name(monkeypatch):
    monkeypatch.setenv("DATABASE_ENGINE", "POSTGRES")
    monkeypatch.delenv("DATABASE_NAME", raising=False)
    settings = PostgresDatabaseSettings()
    assert settings.name == "hr_ms"


def test_postgres_settings_env_override(monkeypatch):
    monkeypatch.setenv("DATABASE_ENGINE", "POSTGRES")
    monkeypatch.setenv("DATABASE_HOST", "db.internal")
    monkeypatch.setenv("DATABASE_PORT", "5433")
    settings = PostgresDatabaseSettings()
    assert settings.host == "db.internal"
    assert settings.port == 5433


# ─── DjangoDatabases ──────────────────────────────────────────────────────────

def test_django_databases_wraps_sqlite():
    db = DjangoDatabases(default=SqliteDatabaseSettings())
    assert db.default.engine == DBEngineEnum.SQLITE


def test_django_databases_wraps_postgres():
    db = DjangoDatabases(default=PostgresDatabaseSettings(_env_file=None))
    assert db.default.engine == DBEngineEnum.POSTGRES


def test_django_databases_model_dump_has_default_key():
    db = DjangoDatabases(default=SqliteDatabaseSettings())
    dumped = db.model_dump(mode="json", by_alias=True)
    assert "default" in dumped
