from django.shortcuts import get_object_or_404

from .models import EmergencyContact, Employee


# ---------------------------------------------------------------------------
# Employee selectors
# ---------------------------------------------------------------------------


def get_employee_list() -> "EmployeeQuerySet":
    return Employee.objects.with_employment().with_user().order_by("last_name", "first_name")


def get_employee(pk) -> Employee:
    return get_object_or_404(Employee.objects.with_employment().with_emergency_contacts().with_user(), pk=pk)


# ---------------------------------------------------------------------------
# EmergencyContact selectors
# ---------------------------------------------------------------------------


def get_emergency_contacts_for_employee(employee_pk) -> "QuerySet":
    return EmergencyContact.objects.filter(employee_id=employee_pk).order_by("-is_primary", "name")


def get_emergency_contact(pk, employee_pk) -> EmergencyContact:
    return get_object_or_404(EmergencyContact, pk=pk, employee_id=employee_pk)
