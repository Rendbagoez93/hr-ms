import datetime

import pytest

from applications.emergency_contact.models import EmergencyContact
from applications.employee.models import Employee, Gender


@pytest.fixture()
def employee_for_emergency(db) -> Employee:
    return Employee.objects.create(
        first_name="Carol",
        last_name="White",
        date_of_birth=datetime.date(1995, 11, 5),
        gender=Gender.FEMALE,
    )


@pytest.fixture()
def emergency_contact(db, employee_for_emergency: Employee) -> EmergencyContact:
    return EmergencyContact.objects.create(
        employee=employee_for_emergency,
        name="David White",
        relationship="Spouse",
        phone_number="08111222333",
        address="Jakarta, Indonesia",
    )
