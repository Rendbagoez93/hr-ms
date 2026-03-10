import pytest

from config.settings.databases import DBEngineEnum
from config.settings.factory import get_django_db_dict


pytestmark = pytest.mark.unit


# ─── Return type ──────────────────────────────────────────────────────────────


def test_returns_a_dict(monkeypatch):
    monkeypatch.delenv("DATABASE_ENGINE", raising=False)
    result = get_django_db_dict()
    assert isinstance(result, dict)


def test_has_default_key(monkeypatch):
    monkeypatch.delenv("DATABASE_ENGINE", raising=False)
    result = get_django_db_dict()
    assert "default" in result


# ─── SQLite (default) ─────────────────────────────────────────────────────────


def test_default_engine_is_sqlite(monkeypatch):
    monkeypatch.delenv("DATABASE_ENGINE", raising=False)
    result = get_django_db_dict()
    assert result["default"]["ENGINE"] == DBEngineEnum.SQLITE


def test_sqlite_dict_has_name_key(monkeypatch):
    monkeypatch.delenv("DATABASE_ENGINE", raising=False)
    result = get_django_db_dict()
    assert "NAME" in result["default"]


def test_sqlite_name_ends_with_db_sqlite3(monkeypatch):
    monkeypatch.delenv("DATABASE_ENGINE", raising=False)
    monkeypatch.delenv("DATABASE_NAME", raising=False)
    result = get_django_db_dict()
    assert str(result["default"]["NAME"]) == "hr_ms"


# ─── PostgreSQL ───────────────────────────────────────────────────────────────


def test_postgres_engine_selected_by_env(monkeypatch):
    monkeypatch.setenv("DATABASE_ENGINE", "POSTGRES")
    result = get_django_db_dict()
    assert result["default"]["ENGINE"] == DBEngineEnum.POSTGRES


def test_postgres_dict_has_host_and_port(monkeypatch):
    monkeypatch.setenv("DATABASE_ENGINE", "POSTGRES")
    result = get_django_db_dict()
    assert "HOST" in result["default"]
    assert "PORT" in result["default"]


def test_postgres_default_host(monkeypatch):
    monkeypatch.setenv("DATABASE_ENGINE", "POSTGRES")
    monkeypatch.delenv("DATABASE_HOST", raising=False)
    result = get_django_db_dict()
    assert result["default"]["HOST"] == "localhost"


def test_postgres_env_host_override(monkeypatch):
    monkeypatch.setenv("DATABASE_ENGINE", "POSTGRES")
    monkeypatch.setenv("DATABASE_HOST", "db.prod.internal")
    result = get_django_db_dict()
    assert result["default"]["HOST"] == "db.prod.internal"
