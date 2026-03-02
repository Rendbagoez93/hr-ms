from config.settings.companyconf import load_company_config
from django.db import connection, models
from shared.base_models import BaseModel

import pytest


# ─── Company config ───────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def company_config():
    return load_company_config()


# ─── Concrete model for BaseModel tests ──────────────────────────────────────
# Creates the table once per session; individual tests use `db` so their rows
# are rolled back automatically after each test.

@pytest.fixture(scope="session")
def _item_model_class(django_db_setup, django_db_blocker):
    class Item(BaseModel):
        name = models.CharField(max_length=100)

        class Meta:
            app_label = "tests_shared"

    with django_db_blocker.unblock():
        with connection.schema_editor() as editor:
            editor.create_model(Item)

    yield Item

    with django_db_blocker.unblock():
        with connection.schema_editor() as editor:
            editor.delete_model(Item)


@pytest.fixture()
def Item(db, _item_model_class):  # noqa: N802
    """Function-scoped alias — rows are rolled back after every test."""
    return _item_model_class
