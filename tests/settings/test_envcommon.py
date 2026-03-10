from pydantic import ValidationError
import pytest

from config.settings.envcommon import EnvSettings


pytestmark = pytest.mark.unit


_KNOWN_ENV_KEYS = ("SECRET_KEY", "DEBUG", "ENVIRONMENT", "ALLOWED_HOSTS", "LANGUAGE_CODE", "CORS_ALLOWED_ORIGINS")

_SENTINEL_SECRET_KEY = "test-only-secret-key-do-not-use-in-production"


def _fresh(monkeypatch, **overrides) -> EnvSettings:
    """Return a new EnvSettings instance with only the given env vars active.

    SECRET_KEY is always injected with a sentinel value unless the caller
    explicitly overrides it, because it has no default.
    """
    for key in _KNOWN_ENV_KEYS:
        monkeypatch.delenv(key, raising=False)
    overrides.setdefault("SECRET_KEY", _SENTINEL_SECRET_KEY)
    for key, val in overrides.items():
        monkeypatch.setenv(key, val)
    return EnvSettings(_env_file=None)


# ─── Defaults ─────────────────────────────────────────────────────────────────


def test_secret_key_is_required(monkeypatch):
    for key in _KNOWN_ENV_KEYS:
        monkeypatch.delenv(key, raising=False)
    with pytest.raises(ValidationError):
        EnvSettings(_env_file=None)


def test_default_debug_is_false(monkeypatch):
    settings = _fresh(monkeypatch)
    assert settings.DEBUG is False


def test_default_environment_is_local(monkeypatch):
    settings = _fresh(monkeypatch)
    assert settings.ENVIRONMENT == "local"


def test_default_allowed_hosts(monkeypatch):
    settings = _fresh(monkeypatch)
    assert "localhost" in settings.ALLOWED_HOSTS
    assert "127.0.0.1" in settings.ALLOWED_HOSTS


def test_default_cors_allowed_origins_empty(monkeypatch):
    settings = _fresh(monkeypatch)
    assert settings.CORS_ALLOWED_ORIGINS == []


def test_default_language_code(monkeypatch):
    settings = _fresh(monkeypatch)
    assert settings.LANGUAGE_CODE == "en-us"


# ─── Env var overrides ────────────────────────────────────────────────────────


def test_override_debug_true(monkeypatch):
    settings = _fresh(monkeypatch, DEBUG="True")
    assert settings.DEBUG is True


def test_override_environment(monkeypatch):
    settings = _fresh(monkeypatch, ENVIRONMENT="production")
    assert settings.ENVIRONMENT == "production"


def test_override_secret_key(monkeypatch):
    settings = _fresh(monkeypatch, SECRET_KEY="super-secret")
    assert settings.SECRET_KEY == "super-secret"


def test_override_language_code(monkeypatch):
    settings = _fresh(monkeypatch, LANGUAGE_CODE="id")
    assert settings.LANGUAGE_CODE == "id"
