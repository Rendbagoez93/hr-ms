import pytest
from rest_framework.test import APIClient

from config.roles import Role
from modules.user.models import User

USER_PASSWORD = "TestPass123!"


@pytest.fixture
def user_password() -> str:
    return USER_PASSWORD


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def create_user(db):
    def _factory(email: str, password: str = USER_PASSWORD, role: str = Role.STAFF, **kwargs):
        return User.objects.create_user(email=email, password=password, role=role, **kwargs)
    return _factory


@pytest.fixture
def active_user(create_user):
    return create_user(email="active@example.com")


@pytest.fixture
def staff_user(create_user):
    return create_user(email="staff@example.com", role=Role.STAFF)


@pytest.fixture
def executive_user(create_user):
    return create_user(email="executive@example.com", role=Role.CEO)


@pytest.fixture
def manager_user(create_user):
    return create_user(email="manager@example.com", role=Role.MANAGER)


@pytest.fixture
def hr_user(create_user):
    return create_user(email="hr@example.com", role=Role.HR_MANAGER)


@pytest.fixture
def finance_user(create_user):
    return create_user(email="finance@example.com", role=Role.FINANCE_MANAGER)


@pytest.fixture
def it_user(create_user):
    return create_user(email="it@example.com", role=Role.IT_MANAGER)
