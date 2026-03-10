from __future__ import annotations

from django.shortcuts import get_object_or_404

from .managers import ContractQuerySet, EmploymentQuerySet, SalaryQuerySet
from .models import Contract, Employment, Salary


# ---------------------------------------------------------------------------
# Employment selectors
# ---------------------------------------------------------------------------


def get_employment_list() -> EmploymentQuerySet:
    return Employment.objects.with_full_detail().order_by("employee__last_name")


def get_employment(pk) -> Employment:
    return get_object_or_404(Employment.objects.with_full_detail(), pk=pk)


def get_employment_for_employee(employee_pk) -> Employment:
    return get_object_or_404(Employment.objects.with_full_detail(), employee_id=employee_pk)


# ---------------------------------------------------------------------------
# Contract selectors
# ---------------------------------------------------------------------------


def get_contracts_for_employment(employment_pk) -> ContractQuerySet:
    return Contract.objects.filter(employment_id=employment_pk).order_by("-start_date")


def get_contract(pk, employment_pk) -> Contract:
    return get_object_or_404(Contract, pk=pk, employment_id=employment_pk)


# ---------------------------------------------------------------------------
# Salary selectors
# ---------------------------------------------------------------------------


def get_salary_history(employment_pk) -> SalaryQuerySet:
    return Salary.objects.filter(employment_id=employment_pk).order_by("-effective_date")


def get_salary(pk, employment_pk) -> Salary:
    return get_object_or_404(Salary, pk=pk, employment_id=employment_pk)
