from .databases import (
    BaseDatabaseSettings,
    DBEngineEnum,
    DjangoDatabases,
    PostgresDatabaseSettings,
    SqliteDatabaseSettings,
)


def get_django_db_dict() -> dict:
    """Build the Django DATABASES dict based on the DATABASE_ENGINE env var."""
    base = BaseDatabaseSettings()
    db_settings = PostgresDatabaseSettings() if base.engine == DBEngineEnum.POSTGRES else SqliteDatabaseSettings()
    return DjangoDatabases(default=db_settings).model_dump(mode="json", by_alias=True)
