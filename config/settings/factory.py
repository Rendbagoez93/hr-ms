"""
Configuration factory using dependency injection.
Builds and provides configuration instances for the Django application.
"""

from typing import Any

from dependency_injector import containers, providers

from .compconfig import CompanySettings, get_company_settings
from .databases import DatabaseConfig, DatabaseFactory
from .envcommon import CommonSettings, DevelopmentSettings, ProductionSettings


def _get_environment_settings(environment: str | None = None) -> CommonSettings:
    if environment is None:
        # Auto-detect from environment variable or default to development
        return DevelopmentSettings()

    environment = environment.lower()

    if environment == "development":
        return DevelopmentSettings()
    elif environment == "production":
        return ProductionSettings()
    else:
        raise ValueError(
            f"Unsupported environment: {environment}. "
            "Must be 'development' or 'production'."
        )


def _build_settings(
    env_settings: CommonSettings,
    db_config: DatabaseConfig,
    company_config: CompanySettings,
) -> dict[str, Any]:

    return {
        "environment": env_settings.environment.value,
        "secret_key": env_settings.secret_key,
        "debug": env_settings.debug,
        "allowed_hosts": env_settings.allowed_hosts,
        "base_dir": env_settings.base_dir,
        "language_code": env_settings.language_code,
        "time_zone": env_settings.time_zone,
        "use_i18n": env_settings.use_i18n,
        "use_tz": env_settings.use_tz,
        "databases": db_config.get_config(),
        "cors_allowed_origins": env_settings.cors_allowed_origins,
        "is_development": env_settings.is_development,
        "is_production": env_settings.is_production,
        "company": company_config.to_dict(),
        "company_context": company_config.get_company_context(),
    }


class ConfigContainer(containers.DeclarativeContainer):
    # Configuration providers
    config = providers.Configuration()

    # Environment settings singleton
    environment_settings = providers.Singleton(
        _get_environment_settings,
        environment=config.environment,
    )

    # Database configuration factory
    database_config = providers.Factory(
        DatabaseFactory.create,
        environment=config.environment,
    )

    # Company configuration singleton
    company_config = providers.Singleton(
        get_company_settings,
        yaml_file=None,
    )

    # Combined settings provider
    settings = providers.Singleton(
        _build_settings,
        env_settings=environment_settings,
        db_config=database_config,
        company_config=company_config,
    )


class SettingsBuilder:
    def __init__(self, environment: str | None = None):
        self.container = ConfigContainer()
        self.environment = environment or "development"
        self.container.config.environment.from_value(self.environment)

    def build(self) -> dict[str, Any]:
        """
        Build complete settings configuration.

        Returns:
            dict: Complete Django settings dictionary.
        """
        return self.container.settings()

    def get_environment_settings(self) -> CommonSettings:
        return self.container.environment_settings()

    def get_database_config(self) -> DatabaseConfig:
        return self.container.database_config()

    def get_company_config(self) -> CompanySettings:
        return self.container.company_config()

    @classmethod
    def build_for_environment(cls, environment: str) -> dict[str, Any]:
        builder = cls(environment=environment)
        return builder.build()


def get_settings_dict(environment: str | None = None) -> dict[str, Any]:
    builder = SettingsBuilder(environment=environment)
    return builder.build()
