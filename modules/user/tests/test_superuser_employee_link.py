import pytest

from applications.employee.models import Employee
from modules.user.models import User


pytestmark = pytest.mark.django_db


def test_create_superuser_auto_creates_employee_profile():
    user = User.objects.create_superuser(
        email="admin.auto@example.com",
        password="TestPass123!",
    )

    employee = Employee.objects.get(user=user)

    assert employee.personal_email == user.email
    assert employee.gender == "prefer_not_to_say"
    assert employee.employee_id.startswith("EMP-SU-")


def test_create_superuser_uses_existing_names_for_employee_profile():
    user = User.objects.create_superuser(
        email="named.admin@example.com",
        password="TestPass123!",
        first_name="Rendy",
        last_name="Bagoez",
    )

    employee = Employee.objects.get(user=user)

    assert employee.first_name == "Rendy"
    assert employee.last_name == "Bagoez"


def test_create_user_does_not_auto_create_employee_profile():
    user = User.objects.create_user(
        email="staff.member@example.com",
        password="TestPass123!",
    )

    assert not Employee.objects.filter(user=user).exists()
