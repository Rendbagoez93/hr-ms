import datetime

import pytest

from applications.department.models import Department
from applications.employee.models import Employee, Gender
from applications.employment.models import EmploymentDetail, EmploymentStatus, WorkLocationType
from applications.job_title.models import JobTitle


@pytest.fixture()
def employment_detail(db) -> EmploymentDetail:
    department = Department.objects.create(name="Engineering")
    job_title = JobTitle.objects.create(title="Software Engineer")
    employee = Employee.objects.create(
        first_name="John",
        last_name="Doe",
        date_of_birth=datetime.date(1990, 1, 15),
        gender=Gender.MALE,
    )
    return EmploymentDetail.objects.create(
        employee=employee,
        department=department,
        job_title=job_title,
        employment_status=EmploymentStatus.FULL_TIME,
        work_location_type=WorkLocationType.ON_SITE,
        start_date=datetime.date(2022, 3, 1),
    )
