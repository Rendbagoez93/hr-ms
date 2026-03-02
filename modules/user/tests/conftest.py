import pytest
from modules.user.models import User
from config.roles import Role


@pytest.fixture()
def create_user(db):
    def _factory(email, password="TestPass123!", role=Role.STAFF, **kwargs):
        return User.objects.create_user(email=email, password=password, role=role, **kwargs)
    return _factory


@pytest.fixture()
def staff_user(create_user):
    return create_user(email="staff@example.com", role=Role.STAFF)


@pytest.fixture()
def hr_manager_user(create_user):
    return create_user(email="hr.manager@example.com", role=Role.HR_MANAGER)


@pytest.fixture()
def ex_employee(create_user):
    """A user to be soft-deleted within the test."""
    return create_user(email="ex.employee@example.com", role=Role.STAFF)
