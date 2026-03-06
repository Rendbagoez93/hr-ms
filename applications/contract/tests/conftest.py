import datetime

import pytest

from applications.contract.models import Contract, ContractType
from applications.employee.models import Employee, Gender


@pytest.fixture()
def employee_for_contract(db) -> Employee:
    return Employee.objects.create(
        first_name="Alice",
        last_name="Johnson",
        date_of_birth=datetime.date(1988, 4, 10),
        gender=Gender.FEMALE,
    )


@pytest.fixture()
def permanent_contract(db, employee_for_contract: Employee) -> Contract:
    return Contract.objects.create(
        employee=employee_for_contract,
        contract_type=ContractType.PERMANENT,
        start_date=datetime.date(2020, 1, 1),
    )


@pytest.fixture()
def fixed_term_contract(db, employee_for_contract: Employee) -> Contract:
    return Contract.objects.create(
        employee=employee_for_contract,
        contract_type=ContractType.FIXED_TERM,
        start_date=datetime.date(2024, 1, 1),
        end_date=datetime.date(2024, 12, 31),
    )
