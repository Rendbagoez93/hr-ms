import pytest
from rest_framework.test import APIClient

from config.roles import Role
from modules.factories import DEFAULT_PASSWORD, UserFactory


@pytest.fixture
def user_password() -> str:
    return DEFAULT_PASSWORD


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def create_user(db):
    return UserFactory.create


@pytest.fixture
def active_user(db):
    return UserFactory(email="active@example.com")


@pytest.fixture
def staff_user(db):
    return UserFactory(email="staff@example.com", role=Role.STAFF)


@pytest.fixture
def executive_user(db):
    return UserFactory(email="executive@example.com", role=Role.CEO)


@pytest.fixture
def manager_user(db):
    return UserFactory(email="manager@example.com", role=Role.MANAGER)


@pytest.fixture
def hr_user(db):
    return UserFactory(email="hr@example.com", role=Role.HR_MANAGER)


@pytest.fixture
def finance_user(db):
    return UserFactory(email="finance@example.com", role=Role.FINANCE_MANAGER)


@pytest.fixture
def it_user(db):
    return UserFactory(email="it@example.com", role=Role.IT_MANAGER)
