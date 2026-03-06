import datetime

import pytest

from applications.employee.models import Employee, Gender


@pytest.fixture()
def employee(db) -> Employee:
    return Employee.objects.create(
        first_name="John",
        last_name="Doe",
        date_of_birth=datetime.date(1990, 1, 15),
        gender=Gender.MALE,
        phone_number="08123456789",
        address="Jakarta, Indonesia",
    )


@pytest.fixture()
def employee_female(db) -> Employee:
    return Employee.objects.create(
        first_name="Jane",
        last_name="Smith",
        date_of_birth=datetime.date(1992, 6, 20),
        gender=Gender.FEMALE,
        phone_number="08198765432",
        address="Bandung, Indonesia",
    )
