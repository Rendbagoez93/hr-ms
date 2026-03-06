import pytest

from applications.job_title.models import JobTitle


@pytest.fixture()
def job_title(db) -> JobTitle:
    return JobTitle.objects.create(title="Software Engineer", description="Develops and maintains software systems")


@pytest.fixture()
def hr_job_title(db) -> JobTitle:
    return JobTitle.objects.create(title="HR Manager", description="Manages human resource operations")
