import pytest

from config.roles import Role
from modules.factories import UserFactory


@pytest.fixture()
def create_user(db):
    return UserFactory.create


@pytest.fixture()
def staff_user(db):
    return UserFactory(email="staff@example.com", role=Role.STAFF)


@pytest.fixture()
def hr_manager_user(db):
    return UserFactory(email="hr.manager@example.com", role=Role.HR_MANAGER)


@pytest.fixture()
def ex_employee(db):
    """A user to be soft-deleted within the test."""
    return UserFactory(email="ex.employee@example.com", role=Role.STAFF)
