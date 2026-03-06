import pytest

from applications.department.models import Department


@pytest.fixture()
def department(db) -> Department:
    return Department.objects.create(name="Engineering", description="Software engineering department")


@pytest.fixture()
def hr_department(db) -> Department:
    return Department.objects.create(name="Human Resources", description="HR department")
