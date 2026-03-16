import pytest

from applications.factories import AttendanceRecordFactory, EmployeeFactory, LeaveRequestFactory, WorkScheduleFactory


@pytest.fixture
def employee(db):
    return EmployeeFactory()


@pytest.fixture
def attendance_record(db):
    return AttendanceRecordFactory()


@pytest.fixture
def leave_request(db):
    return LeaveRequestFactory()


@pytest.fixture
def work_schedule(db):
    return WorkScheduleFactory()
