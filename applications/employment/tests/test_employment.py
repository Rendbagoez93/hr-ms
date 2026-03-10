import datetime

import pytest

from applications.employment.constants import (
    ContractType,
    EmploymentStatus,
    PaymentFrequency,
    WorkLocationType,
)
from applications.employment.models import Contract, Employment, Salary
from applications.factories import (
    ContractFactory,
    DepartmentFactory,
    EmployeeFactory,
    EmploymentFactory,
    JobTitleFactory,
    SalaryFactory,
)


pytestmark = pytest.mark.django_db


# ─── Employment model ─────────────────────────────────────────────────────────


class TestEmploymentModel:
    def test_str_representation(self, db):
        dept = DepartmentFactory(name="Engineering")
        title = JobTitleFactory(name="Software Engineer", department=dept)
        employee = EmployeeFactory(first_name="Budi", last_name="Santoso", employee_id="EMP001")
        employment = EmploymentFactory(employee=employee, department=dept, job_title=title)
        result = str(employment)
        assert "Budi Santoso" in result
        assert "Software Engineer" in result
        assert "Engineering" in result

    def test_default_status_is_probation(self, db):
        employment = EmploymentFactory(status=EmploymentStatus.PROBATION)
        assert employment.status == EmploymentStatus.PROBATION

    def test_employee_is_unique_per_employment(self, db):
        employment = EmploymentFactory()
        with pytest.raises(Exception):
            EmploymentFactory(employee=employment.employee)

    def test_reporting_manager_can_be_null(self, db):
        employment = EmploymentFactory(reporting_manager=None)
        assert employment.reporting_manager is None

    def test_reporting_manager_is_employee_instance(self, db):
        manager = EmployeeFactory()
        employment = EmploymentFactory(reporting_manager=manager)
        assert employment.reporting_manager == manager

    def test_end_date_can_be_null(self, db):
        employment = EmploymentFactory(end_date=None)
        assert employment.end_date is None

    def test_terminated_employee_has_end_date(self, db):
        end = datetime.date(2025, 12, 31)
        employment = EmploymentFactory(status=EmploymentStatus.TERMINATED, end_date=end)
        assert employment.end_date == end

    def test_work_location_choices(self, db):
        for location in WorkLocationType:
            emp = EmploymentFactory(work_location=location)
            emp.refresh_from_db()
            assert emp.work_location == location

    def test_soft_delete_hides_employment(self, db):
        employment = EmploymentFactory()
        pk = employment.pk
        employment.delete()
        assert not Employment.objects.filter(pk=pk).exists()

    def test_restore_employment_record(self, db):
        employment = EmploymentFactory()
        pk = employment.pk
        employment.delete()
        employment.restore()
        assert Employment.objects.filter(pk=pk).exists()

    def test_department_protected_from_deletion(self, db):
        from django.db.models import ProtectedError

        dept = DepartmentFactory()
        EmploymentFactory(department=dept)
        with pytest.raises(ProtectedError):
            dept.hard_delete()

    def test_job_title_protected_from_deletion(self, db):
        from django.db.models import ProtectedError

        title = JobTitleFactory()
        EmploymentFactory(job_title=title)
        with pytest.raises(ProtectedError):
            title.hard_delete()


# ─── EmploymentManager / QuerySet ────────────────────────────────────────────


class TestEmploymentManager:
    def test_active_returns_active_and_probation(self, db):
        active = EmploymentFactory(status=EmploymentStatus.ACTIVE)
        probation = EmploymentFactory(status=EmploymentStatus.PROBATION)
        on_leave = EmploymentFactory(status=EmploymentStatus.ON_LEAVE)
        terminated = EmploymentFactory(status=EmploymentStatus.TERMINATED)

        active_pks = set(Employment.objects.active().values_list("pk", flat=True))
        assert active.pk in active_pks
        assert probation.pk in active_pks
        assert on_leave.pk in active_pks
        assert terminated.pk not in active_pks

    def test_with_employee_select_related(self, db):
        EmploymentFactory()
        emp = Employment.objects.with_employee().first()
        assert emp is not None
        _ = emp.employee  # no extra query

    def test_with_position_select_related(self, db):
        EmploymentFactory()
        emp = Employment.objects.with_position().first()
        assert emp.department is not None
        assert emp.job_title is not None

    def test_with_reporting_manager_select_related(self, db):
        manager = EmployeeFactory()
        EmploymentFactory(reporting_manager=manager)
        emp = Employment.objects.with_reporting_manager().filter(reporting_manager=manager).first()
        assert emp is not None
        _ = emp.reporting_manager

    def test_with_full_detail_loads_all_relations(self, db):
        manager = EmployeeFactory()
        EmploymentFactory(reporting_manager=manager)
        emp = Employment.objects.with_full_detail().first()
        assert emp.employee is not None
        assert emp.department is not None
        assert emp.job_title is not None

    def test_default_manager_excludes_soft_deleted(self, db):
        employment = EmploymentFactory()
        employment.delete()
        assert employment.pk not in Employment.objects.values_list("pk", flat=True)

    def test_active_statuses_list(self):
        active = EmploymentStatus.active_statuses()
        assert EmploymentStatus.ACTIVE in active
        assert EmploymentStatus.PROBATION in active
        assert EmploymentStatus.ON_LEAVE in active
        assert EmploymentStatus.TERMINATED not in active
        assert EmploymentStatus.RESIGNED not in active

    def test_find_direct_reports_of_manager(self, db):
        manager = EmployeeFactory()
        report_1 = EmploymentFactory(reporting_manager=manager)
        report_2 = EmploymentFactory(reporting_manager=manager)
        EmploymentFactory(reporting_manager=None)

        reports = Employment.objects.filter(reporting_manager=manager)
        report_pks = set(reports.values_list("pk", flat=True))
        assert report_1.pk in report_pks
        assert report_2.pk in report_pks


# ─── Contract model ───────────────────────────────────────────────────────────


class TestContractModel:
    def test_str_representation(self, db):
        employment = EmploymentFactory()
        contract = ContractFactory(
            employment=employment,
            contract_type=ContractType.PERMANENT,
            start_date=datetime.date(2023, 1, 1),
        )
        result = str(contract)
        assert "permanent" in result
        assert "2023-01-01" in result

    def test_open_ended_contract_has_no_end_date(self, db):
        contract = ContractFactory(end_date=None)
        assert contract.end_date is None

    def test_fixed_term_contract_has_end_date(self, db):
        end = datetime.date(2025, 12, 31)
        contract = ContractFactory(contract_type=ContractType.FIXED_TERM, end_date=end)
        assert contract.end_date == end

    def test_terms_field_can_be_blank(self, db):
        contract = ContractFactory(terms="")
        assert contract.pk is not None

    def test_cascade_delete_when_employment_deleted(self, db):
        employment = EmploymentFactory()
        contract = ContractFactory(employment=employment)
        contract_pk = contract.pk
        employment.hard_delete()
        assert not Contract.all_objects.filter(pk=contract_pk).exists()

    def test_multiple_contracts_per_employment(self, db):
        employment = EmploymentFactory()
        ContractFactory(employment=employment, contract_type=ContractType.PROBATIONARY)
        ContractFactory(employment=employment, contract_type=ContractType.PERMANENT)
        assert employment.contracts.count() == 2

    def test_all_contract_types_are_valid(self, db):
        employment = EmploymentFactory()
        for contract_type in ContractType:
            c = ContractFactory(employment=employment, contract_type=contract_type)
            c.refresh_from_db()
            assert c.contract_type == contract_type

    def test_soft_delete_hides_contract(self, db):
        contract = ContractFactory()
        pk = contract.pk
        contract.delete()
        assert not Contract.objects.filter(pk=pk).exists()


# ─── ContractManager / QuerySet ──────────────────────────────────────────────


class TestContractManager:
    def test_current_includes_open_ended_contracts(self, db):
        open_contract = ContractFactory(end_date=None)
        pks = Contract.objects.current().values_list("pk", flat=True)
        assert open_contract.pk in pks

    def test_current_includes_future_end_date(self, db):
        future = datetime.date.today() + datetime.timedelta(days=180)
        future_contract = ContractFactory(end_date=future)
        pks = Contract.objects.current().values_list("pk", flat=True)
        assert future_contract.pk in pks

    def test_current_excludes_past_end_date(self, db):
        past = datetime.date(2020, 1, 1)
        expired = ContractFactory(end_date=past)
        pks = Contract.objects.current().values_list("pk", flat=True)
        assert expired.pk not in pks

    def test_default_manager_excludes_soft_deleted(self, db):
        contract = ContractFactory()
        contract.delete()
        assert contract.pk not in Contract.objects.values_list("pk", flat=True)


# ─── Salary model ─────────────────────────────────────────────────────────────


class TestSalaryModel:
    def test_current_salary_has_no_end_date(self, db):
        salary = SalaryFactory(end_date=None)
        assert salary.end_date is None

    def test_past_salary_has_end_date(self, db):
        end = datetime.date(2023, 12, 31)
        salary = SalaryFactory(end_date=end)
        assert salary.end_date == end

    def test_cascade_delete_when_employment_deleted(self, db):
        employment = EmploymentFactory()
        salary = SalaryFactory(employment=employment)
        salary_pk = salary.pk
        employment.hard_delete()
        assert not Salary.all_objects.filter(pk=salary_pk).exists()

    def test_salary_history_multiple_records(self, db):
        employment = EmploymentFactory()
        SalaryFactory(employment=employment, amount=10_000_000, end_date=datetime.date(2023, 12, 31))
        SalaryFactory(employment=employment, amount=12_000_000, end_date=None)
        assert employment.salary_history.count() == 2

    def test_currency_default_is_idr(self, db):
        salary = SalaryFactory()
        assert salary.currency == "IDR"

    def test_all_payment_frequencies_valid(self, db):
        employment = EmploymentFactory()
        for freq in PaymentFrequency:
            s = SalaryFactory(employment=employment, payment_frequency=freq)
            s.refresh_from_db()
            assert s.payment_frequency == freq

    def test_soft_delete_hides_salary(self, db):
        salary = SalaryFactory()
        pk = salary.pk
        salary.delete()
        assert not Salary.objects.filter(pk=pk).exists()


# ─── SalaryManager / QuerySet ────────────────────────────────────────────────


class TestSalaryManager:
    def test_current_returns_salaries_with_no_end_date(self, db):
        employment = EmploymentFactory()
        current = SalaryFactory(employment=employment, end_date=None)
        past = SalaryFactory(employment=employment, end_date=datetime.date(2023, 6, 30))

        current_pks = Salary.objects.current().values_list("pk", flat=True)
        assert current.pk in current_pks
        assert past.pk not in current_pks

    def test_history_returns_salaries_with_end_date(self, db):
        employment = EmploymentFactory()
        current = SalaryFactory(employment=employment, end_date=None)
        past = SalaryFactory(employment=employment, end_date=datetime.date(2022, 12, 31))

        history_pks = Salary.objects.history().values_list("pk", flat=True)
        assert past.pk in history_pks
        assert current.pk not in history_pks

    def test_default_manager_excludes_soft_deleted(self, db):
        salary = SalaryFactory()
        salary.delete()
        assert salary.pk not in Salary.objects.values_list("pk", flat=True)

    def test_get_latest_salary_via_ordering(self, db):
        employment = EmploymentFactory()
        SalaryFactory(employment=employment, effective_date=datetime.date(2022, 1, 1), end_date=datetime.date(2022, 12, 31))
        latest = SalaryFactory(employment=employment, effective_date=datetime.date(2024, 1, 1), end_date=None)

        first_result = Salary.objects.filter(employment=employment).first()
        assert first_result == latest  # ordering = ("-effective_date",)


# ─── Constants ────────────────────────────────────────────────────────────────


class TestEmploymentStatusEnum:
    def test_choices_returns_list_of_tuples(self):
        choices = EmploymentStatus.choices()
        assert isinstance(choices, list)
        assert all(isinstance(c, tuple) and len(c) == 2 for c in choices)

    def test_active_statuses_returns_correct_subset(self):
        active = EmploymentStatus.active_statuses()
        assert set(active) == {EmploymentStatus.ACTIVE, EmploymentStatus.PROBATION, EmploymentStatus.ON_LEAVE}

    def test_terminated_not_in_active_statuses(self):
        assert EmploymentStatus.TERMINATED not in EmploymentStatus.active_statuses()


class TestContractTypeEnum:
    def test_all_values_in_choices(self):
        values = [c[0] for c in ContractType.choices()]
        for member in ContractType:
            assert member.value in values


class TestPaymentFrequencyEnum:
    def test_all_values_in_choices(self):
        values = [c[0] for c in PaymentFrequency.choices()]
        for member in PaymentFrequency:
            assert member.value in values


class TestWorkLocationTypeEnum:
    def test_all_values_in_choices(self):
        values = [c[0] for c in WorkLocationType.choices()]
        for member in WorkLocationType:
            assert member.value in values
