"""
Factories for application-level models.

All factories follow the factory_boy convention and can be used in tests
without relying on conftest.py fixtures.
"""

import datetime

import factory
from factory.django import DjangoModelFactory

from applications.attendance.constants import AttendanceStatus, LeaveStatus, LeaveType
from applications.attendance.models import AttendanceRecord, LeaveRequest, WorkSchedule
from applications.employee.constants import EmergencyContactRelationship, Gender
from applications.employee.models import EmergencyContact, Employee
from applications.employment.constants import (
    ContractType,
    EmploymentStatus,
    PaymentFrequency,
    WorkLocationType,
)
from applications.employment.models import Contract, Employment, Salary
from applications.organization.models import Department, JobTitle
from modules.factories import UserFactory


class DepartmentFactory(DjangoModelFactory):
    class Meta:
        model = Department

    name = factory.Sequence(lambda n: f"Department {n}")
    code = factory.Sequence(lambda n: f"DEPT{n:03d}")
    description = factory.Faker("sentence")
    parent = None


class JobTitleFactory(DjangoModelFactory):
    class Meta:
        model = JobTitle

    name = factory.Sequence(lambda n: f"Job Title {n}")
    code = factory.Sequence(lambda n: f"JOB{n:03d}")
    description = factory.Faker("sentence")
    department = factory.SubFactory(DepartmentFactory)


class EmployeeFactory(DjangoModelFactory):
    class Meta:
        model = Employee

    user = factory.SubFactory(UserFactory)
    employee_id = factory.Sequence(lambda n: f"EMP{n:04d}")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    date_of_birth = factory.Faker("date_of_birth", minimum_age=18, maximum_age=60)
    gender = Gender.MALE
    nationality = "Indonesian"
    national_id = factory.Sequence(lambda n: f"ID{n:010d}")
    phone = factory.Faker("phone_number")
    personal_email = factory.Faker("email")
    address_line_1 = factory.Faker("street_address")
    city = factory.Faker("city")
    country = "Indonesia"


class EmergencyContactFactory(DjangoModelFactory):
    class Meta:
        model = EmergencyContact

    employee = factory.SubFactory(EmployeeFactory)
    name = factory.Faker("name")
    relationship = EmergencyContactRelationship.SPOUSE
    phone = factory.Faker("phone_number")
    email = factory.Faker("email")
    address = factory.Faker("address")
    is_primary = False


class EmploymentFactory(DjangoModelFactory):
    class Meta:
        model = Employment

    employee = factory.SubFactory(EmployeeFactory)
    department = factory.SubFactory(DepartmentFactory)
    job_title = factory.SubFactory(JobTitleFactory)
    reporting_manager = None
    work_location = WorkLocationType.ONSITE
    status = EmploymentStatus.ACTIVE
    hire_date = factory.Faker("date_between", start_date="-5y", end_date="-1y")
    end_date = None


class ContractFactory(DjangoModelFactory):
    class Meta:
        model = Contract

    employment = factory.SubFactory(EmploymentFactory)
    contract_type = ContractType.PERMANENT
    start_date = factory.Faker("date_between", start_date="-5y", end_date="-1y")
    end_date = None
    terms = factory.Faker("paragraph")


class SalaryFactory(DjangoModelFactory):
    class Meta:
        model = Salary

    employment = factory.SubFactory(EmploymentFactory)
    pay_grade = factory.Sequence(lambda n: f"G{n % 5 + 1}")
    amount = factory.Faker("pydecimal", left_digits=9, right_digits=2, positive=True)
    currency = "IDR"
    payment_frequency = PaymentFrequency.MONTHLY
    effective_date = factory.Faker("date_between", start_date="-5y", end_date="-1y")
    end_date = None
    notes = ""


class WorkScheduleFactory(DjangoModelFactory):
    class Meta:
        model = WorkSchedule

    employee = factory.SubFactory(EmployeeFactory)
    name = "Standard"
    is_default = True
    monday = True
    tuesday = True
    wednesday = True
    thursday = True
    friday = True
    saturday = False
    sunday = False
    expected_check_in = datetime.time(8, 0)
    expected_check_out = datetime.time(17, 0)
    effective_from = factory.Faker("date_between", start_date="-1y", end_date="today")
    effective_to = None


class AttendanceRecordFactory(DjangoModelFactory):
    class Meta:
        model = AttendanceRecord

    employee = factory.SubFactory(EmployeeFactory)
    date = factory.Faker("date_this_year")
    status = AttendanceStatus.PRESENT
    check_in = datetime.time(8, 0)
    check_out = datetime.time(17, 0)
    work_hours = factory.LazyAttribute(lambda _: None)
    late_minutes = 0
    notes = ""


class LeaveRequestFactory(DjangoModelFactory):
    class Meta:
        model = LeaveRequest

    employee = factory.SubFactory(EmployeeFactory)
    leave_type = LeaveType.ANNUAL
    start_date = factory.Faker("date_this_year")
    end_date = factory.LazyAttribute(lambda obj: obj.start_date + datetime.timedelta(days=2))
    total_days = 3
    reason = factory.Faker("sentence")
    status = LeaveStatus.PENDING
    approved_by = None
    approval_notes = ""
    reviewed_at = None
