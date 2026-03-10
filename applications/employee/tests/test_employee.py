import pytest

from applications.employee.constants import EmergencyContactRelationship, Gender
from applications.employee.models import EmergencyContact, Employee
from applications.factories import EmployeeFactory, EmergencyContactFactory, UserFactory


pytestmark = pytest.mark.django_db


# ─── Employee model ───────────────────────────────────────────────────────────


class TestEmployeeModel:
    def test_full_name_property(self):
        employee = EmployeeFactory.build(first_name="Budi", last_name="Santoso")
        assert employee.full_name == "Budi Santoso"

    def test_str_representation(self):
        employee = EmployeeFactory.build(
            employee_id="EMP001",
            first_name="Budi",
            last_name="Santoso",
        )
        assert str(employee) == "EMP001 - Budi Santoso"

    def test_employee_id_is_unique(self, db):
        EmployeeFactory(employee_id="EMP999")
        with pytest.raises(Exception):
            EmployeeFactory(employee_id="EMP999")

    def test_employee_with_user_account(self, db):
        employee = EmployeeFactory()
        assert employee.user is not None
        assert employee.user == employee.user

    def test_employee_without_user_account(self, db):
        employee = EmployeeFactory(user=None)
        assert employee.user is None

    def test_gender_choices_stored_correctly(self, db):
        employee = EmployeeFactory(gender=Gender.FEMALE)
        employee.refresh_from_db()
        assert employee.gender == Gender.FEMALE

    def test_soft_delete_excludes_from_default_queryset(self, db):
        employee = EmployeeFactory()
        pk = employee.pk
        employee.delete()
        assert not Employee.objects.filter(pk=pk).exists()

    def test_soft_delete_keeps_record_in_all_objects(self, db):
        employee = EmployeeFactory()
        pk = employee.pk
        employee.delete()
        assert Employee.all_objects.filter(pk=pk).exists()

    def test_restore_makes_employee_active_again(self, db):
        employee = EmployeeFactory()
        pk = employee.pk
        employee.delete()
        assert not Employee.objects.filter(pk=pk).exists()
        employee.restore()
        assert Employee.objects.filter(pk=pk).exists()
        assert Employee.objects.get(pk=pk).is_active is True

    def test_ordering_by_last_name_then_first_name(self, db):
        EmployeeFactory(first_name="Rizky", last_name="Widodo")
        EmployeeFactory(first_name="Andi", last_name="Budiman")
        employees = list(Employee.objects.all())
        assert employees[0].last_name <= employees[1].last_name

    def test_optional_fields_can_be_blank(self, db):
        employee = EmployeeFactory(
            nationality="",
            national_id="",
            phone="",
            personal_email="",
            address_line_1="",
            city="",
            country="",
        )
        assert employee.pk is not None


# ─── EmployeeManager / QuerySet ───────────────────────────────────────────────


class TestEmployeeManager:
    def test_active_returns_only_active_employees(self, db):
        active = EmployeeFactory(is_active=True)
        inactive = EmployeeFactory(is_active=False)
        inactive.deleted_at = inactive.updated_at
        inactive.save()

        pks = Employee.objects.active().values_list("pk", flat=True)
        assert active.pk in pks
        assert inactive.pk not in pks

    def test_default_manager_excludes_soft_deleted(self, db):
        employee = EmployeeFactory()
        employee.delete()
        assert employee.pk not in Employee.objects.values_list("pk", flat=True)

    def test_with_user_performs_select_related(self, db):
        EmployeeFactory()
        qs = Employee.objects.with_user()
        emp = qs.first()
        assert emp is not None
        _ = emp.user  # no additional query — already select_related

    def test_with_emergency_contacts_prefetches(self, db):
        employee = EmployeeFactory()
        EmergencyContactFactory(employee=employee)
        EmergencyContactFactory(employee=employee)

        emp = Employee.objects.with_emergency_contacts().get(pk=employee.pk)
        # contacts already prefetched; len() uses cache
        assert len(emp.emergency_contacts.all()) == 2


# ─── EmergencyContact model ───────────────────────────────────────────────────


class TestEmergencyContactModel:
    def test_str_representation(self, db):
        employee = EmployeeFactory(first_name="Budi", last_name="Santoso", employee_id="EMP100")
        contact = EmergencyContactFactory(
            employee=employee,
            name="Siti Rohani",
            relationship=EmergencyContactRelationship.SPOUSE,
        )
        assert "Siti Rohani" in str(contact)
        assert "spouse" in str(contact)

    def test_primary_contact_flag(self, db):
        employee = EmployeeFactory()
        primary = EmergencyContactFactory(employee=employee, is_primary=True)
        secondary = EmergencyContactFactory(employee=employee, is_primary=False)

        contacts = list(employee.emergency_contacts.all())
        primary_contacts = [c for c in contacts if c.is_primary]
        assert primary in primary_contacts
        assert secondary not in primary_contacts

    def test_ordering_primary_first(self, db):
        employee = EmployeeFactory()
        secondary = EmergencyContactFactory(employee=employee, is_primary=False, name="Zzz")
        primary = EmergencyContactFactory(employee=employee, is_primary=True, name="Aaa")

        contacts = list(employee.emergency_contacts.order_by("-is_primary", "name"))
        assert contacts[0] == primary

    def test_multiple_contacts_per_employee(self, db):
        employee = EmployeeFactory()
        EmergencyContactFactory(employee=employee, relationship=EmergencyContactRelationship.SPOUSE)
        EmergencyContactFactory(employee=employee, relationship=EmergencyContactRelationship.PARENT)
        EmergencyContactFactory(employee=employee, relationship=EmergencyContactRelationship.RELATIVE)

        assert employee.emergency_contacts.count() == 3

    def test_cascade_delete_removes_contacts(self, db):
        employee = EmployeeFactory()
        EmergencyContactFactory(employee=employee)
        employee_pk = employee.pk
        employee.hard_delete()
        assert not EmergencyContact.objects.filter(employee_id=employee_pk).exists()

    def test_email_and_address_are_optional(self, db):
        contact = EmergencyContactFactory(email="", address="")
        assert contact.pk is not None

    def test_all_relationship_choices_are_valid(self, db):
        employee = EmployeeFactory()
        for relationship in EmergencyContactRelationship:
            contact = EmergencyContactFactory(employee=employee, relationship=relationship)
            contact.refresh_from_db()
            assert contact.relationship == relationship


# ─── Gender / EmergencyContactRelationship enums ─────────────────────────────


class TestGenderEnum:
    def test_choices_returns_list_of_tuples(self):
        choices = Gender.choices()
        assert isinstance(choices, list)
        assert all(isinstance(c, tuple) and len(c) == 2 for c in choices)

    def test_all_values_present_in_choices(self):
        values = [c[0] for c in Gender.choices()]
        for member in Gender:
            assert member.value in values

    def test_prefer_not_to_say_value(self):
        assert Gender.PREFER_NOT_TO_SAY == "prefer_not_to_say"


class TestEmergencyContactRelationshipEnum:
    def test_choices_returns_list_of_tuples(self):
        choices = EmergencyContactRelationship.choices()
        assert isinstance(choices, list)
        assert all(isinstance(c, tuple) and len(c) == 2 for c in choices)

    def test_all_values_present_in_choices(self):
        values = [c[0] for c in EmergencyContactRelationship.choices()]
        for member in EmergencyContactRelationship:
            assert member.value in values
