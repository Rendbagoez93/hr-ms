import datetime
from decimal import Decimal

import pytest

from applications.employee.models import Employee, Gender
from applications.salary.models import PaymentFrequency, Salary


@pytest.fixture()
def employee_for_salary(db) -> Employee:
    return Employee.objects.create(
        first_name="Bob",
        last_name="Brown",
        date_of_birth=datetime.date(1985, 7, 22),
        gender=Gender.MALE,
    )


@pytest.fixture()
def salary(db, employee_for_salary: Employee) -> Salary:
    return Salary.objects.create(
        employee=employee_for_salary,
        pay_grade="G4",
        amount=Decimal("10000000.00"),
        currency="IDR",
        frequency=PaymentFrequency.MONTHLY,
        effective_date=datetime.date(2023, 1, 1),
    )
