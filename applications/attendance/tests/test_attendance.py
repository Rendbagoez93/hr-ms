import datetime

import pytest

from applications.attendance.constants import AttendanceStatus, LeaveStatus, LeaveType
from applications.attendance.models import AttendanceRecord, LeaveRequest, WorkSchedule
from applications.attendance.selectors import (
    get_active_schedule_for_employee,
    get_attendance_record,
    get_leave_request,
    get_work_schedule,
)
from applications.attendance.services import (
    approve_leave_request,
    cancel_leave_request,
    create_attendance_record,
    create_leave_request,
    create_work_schedule,
    delete_attendance_record,
    reject_leave_request,
    update_attendance_record,
)
from applications.factories import AttendanceRecordFactory, EmployeeFactory, LeaveRequestFactory, WorkScheduleFactory


pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------
# WorkSchedule model tests
# ---------------------------------------------------------------------------


class TestWorkScheduleModel:
    def test_str_representation(self):
        schedule = WorkScheduleFactory.build()
        assert schedule.name in str(schedule)

    def test_is_open_ended_when_no_effective_to(self):
        schedule = WorkScheduleFactory.build(effective_to=None)
        assert schedule.is_open_ended is True

    def test_not_open_ended_when_effective_to_set(self):
        schedule = WorkScheduleFactory.build(effective_to=datetime.date(2026, 12, 31))
        assert schedule.is_open_ended is False

    def test_work_days_property_returns_enabled_days(self):
        schedule = WorkScheduleFactory.build(
            monday=True,
            tuesday=True,
            wednesday=True,
            thursday=True,
            friday=True,
            saturday=False,
            sunday=False,
        )
        assert schedule.work_days == ["monday", "tuesday", "wednesday", "thursday", "friday"]

    def test_work_days_empty_when_all_disabled(self):
        schedule = WorkScheduleFactory.build(
            monday=False,
            tuesday=False,
            wednesday=False,
            thursday=False,
            friday=False,
            saturday=False,
            sunday=False,
        )
        assert schedule.work_days == []

    def test_soft_delete_excluded_from_default_manager(self):
        schedule = WorkScheduleFactory()
        pk = schedule.pk
        schedule.delete()
        assert not WorkSchedule.objects.filter(pk=pk).exists()
        assert WorkSchedule.all_objects.filter(pk=pk).exists()

    def test_restore_reenables_schedule(self):
        schedule = WorkScheduleFactory()
        schedule.delete()
        schedule.restore()
        assert WorkSchedule.objects.filter(pk=schedule.pk).exists()


# ---------------------------------------------------------------------------
# AttendanceRecord model tests
# ---------------------------------------------------------------------------


class TestAttendanceRecordModel:
    def test_str_representation(self):
        record = AttendanceRecordFactory.build(status=AttendanceStatus.PRESENT)
        assert AttendanceStatus.PRESENT in str(record)

    def test_str_contains_date(self):
        date = datetime.date(2026, 3, 15)
        record = AttendanceRecordFactory.build(date=date)
        assert "2026-03-15" in str(record)

    def test_soft_delete_excluded_from_default_manager(self):
        record = AttendanceRecordFactory()
        pk = record.pk
        record.delete()
        assert not AttendanceRecord.objects.filter(pk=pk).exists()
        assert AttendanceRecord.all_objects.filter(pk=pk).exists()

    def test_restore_reenables_record(self):
        record = AttendanceRecordFactory()
        record.delete()
        record.restore()
        assert AttendanceRecord.objects.filter(pk=record.pk).exists()


# ---------------------------------------------------------------------------
# LeaveRequest model tests
# ---------------------------------------------------------------------------


class TestLeaveRequestModel:
    def test_str_representation(self):
        leave = LeaveRequestFactory.build()
        assert leave.leave_type in str(leave)

    def test_is_pending_property(self):
        leave = LeaveRequestFactory.build(status=LeaveStatus.PENDING)
        assert leave.is_pending is True

    def test_is_not_pending_when_approved(self):
        leave = LeaveRequestFactory.build(status=LeaveStatus.APPROVED)
        assert leave.is_pending is False

    def test_is_approved_property(self):
        leave = LeaveRequestFactory.build(status=LeaveStatus.APPROVED)
        assert leave.is_approved is True

    def test_soft_delete_excluded_from_default_manager(self):
        leave = LeaveRequestFactory()
        pk = leave.pk
        leave.delete()
        assert not LeaveRequest.objects.filter(pk=pk).exists()
        assert LeaveRequest.all_objects.filter(pk=pk).exists()


# ---------------------------------------------------------------------------
# AttendanceRecord QuerySet tests
# ---------------------------------------------------------------------------


class TestAttendanceRecordQuerySet:
    def test_for_employee_filters_correctly(self):
        emp1 = EmployeeFactory()
        emp2 = EmployeeFactory()
        AttendanceRecordFactory(employee=emp1, date=datetime.date(2026, 1, 5))
        AttendanceRecordFactory(employee=emp2, date=datetime.date(2026, 1, 5))
        assert AttendanceRecord.objects.for_employee(emp1.pk).count() == 1

    def test_for_date_range_returns_correct_records(self):
        emp = EmployeeFactory()
        AttendanceRecordFactory(employee=emp, date=datetime.date(2026, 1, 1))
        AttendanceRecordFactory(employee=emp, date=datetime.date(2026, 1, 15))
        AttendanceRecordFactory(employee=emp, date=datetime.date(2026, 2, 1))
        qs = AttendanceRecord.objects.for_date_range(datetime.date(2026, 1, 1), datetime.date(2026, 1, 31))
        assert qs.count() == 2

    def test_present_returns_only_present_statuses(self):
        emp = EmployeeFactory()
        AttendanceRecordFactory(employee=emp, date=datetime.date(2026, 1, 1), status=AttendanceStatus.PRESENT)
        AttendanceRecordFactory(employee=emp, date=datetime.date(2026, 1, 2), status=AttendanceStatus.ABSENT)
        AttendanceRecordFactory(employee=emp, date=datetime.date(2026, 1, 3), status=AttendanceStatus.LATE)
        assert AttendanceRecord.objects.present().count() == 2

    def test_absent_returns_only_absent_statuses(self):
        emp = EmployeeFactory()
        AttendanceRecordFactory(employee=emp, date=datetime.date(2026, 1, 1), status=AttendanceStatus.PRESENT)
        AttendanceRecordFactory(employee=emp, date=datetime.date(2026, 1, 2), status=AttendanceStatus.ABSENT)
        AttendanceRecordFactory(employee=emp, date=datetime.date(2026, 1, 3), status=AttendanceStatus.ON_LEAVE)
        assert AttendanceRecord.objects.absent().count() == 2


# ---------------------------------------------------------------------------
# Attendance service tests
# ---------------------------------------------------------------------------


class TestCreateAttendanceRecord:
    def test_creates_record_with_work_hours(self):
        emp = EmployeeFactory()
        record = create_attendance_record(
            employee=emp,
            date=datetime.date(2026, 3, 15),
            status=AttendanceStatus.PRESENT,
            check_in=datetime.time(8, 0),
            check_out=datetime.time(17, 0),
        )
        assert record.pk is not None
        assert record.work_hours is not None
        assert float(record.work_hours) == 9.0

    def test_creates_record_without_times(self):
        emp = EmployeeFactory()
        record = create_attendance_record(
            employee=emp,
            date=datetime.date(2026, 3, 15),
            status=AttendanceStatus.ABSENT,
        )
        assert record.work_hours is None
        assert record.late_minutes == 0

    def test_raises_on_duplicate_employee_date(self):
        from django.db import IntegrityError

        emp = EmployeeFactory()
        create_attendance_record(employee=emp, date=datetime.date(2026, 3, 1), status=AttendanceStatus.PRESENT)
        with pytest.raises((IntegrityError, Exception)):
            create_attendance_record(employee=emp, date=datetime.date(2026, 3, 1), status=AttendanceStatus.ABSENT)


class TestUpdateAttendanceRecord:
    def test_updates_status(self):
        record = AttendanceRecordFactory(status=AttendanceStatus.PRESENT)
        updated = update_attendance_record(record.pk, status=AttendanceStatus.LATE)
        assert updated.status == AttendanceStatus.LATE

    def test_recomputes_work_hours_on_time_update(self):
        record = AttendanceRecordFactory(check_in=datetime.time(8, 0), check_out=datetime.time(12, 0))
        updated = update_attendance_record(record.pk, check_out=datetime.time(17, 0))
        assert float(updated.work_hours) == 9.0


class TestDeleteAttendanceRecord:
    def test_soft_deletes_record(self):
        record = AttendanceRecordFactory()
        pk = record.pk
        delete_attendance_record(pk)
        assert not AttendanceRecord.objects.filter(pk=pk).exists()
        assert AttendanceRecord.all_objects.filter(pk=pk).exists()


# ---------------------------------------------------------------------------
# Leave request service tests
# ---------------------------------------------------------------------------


class TestCreateLeaveRequest:
    def test_creates_request_with_correct_total_days(self):
        emp = EmployeeFactory()
        leave = create_leave_request(
            employee=emp,
            leave_type=LeaveType.ANNUAL,
            start_date=datetime.date(2026, 4, 1),
            end_date=datetime.date(2026, 4, 5),
            reason="Annual leave",
        )
        assert leave.total_days == 5
        assert leave.status == LeaveStatus.PENDING

    def test_single_day_leave_has_total_days_one(self):
        emp = EmployeeFactory()
        leave = create_leave_request(
            employee=emp,
            leave_type=LeaveType.SICK,
            start_date=datetime.date(2026, 4, 1),
            end_date=datetime.date(2026, 4, 1),
            reason="Sick",
        )
        assert leave.total_days == 1


class TestApproveLeaveRequest:
    def test_sets_status_approved(self):
        reviewer = EmployeeFactory()
        leave = LeaveRequestFactory(status=LeaveStatus.PENDING)
        updated = approve_leave_request(leave.pk, reviewed_by=reviewer, notes="Approved.")
        assert updated.status == LeaveStatus.APPROVED
        assert updated.approved_by == reviewer
        assert updated.reviewed_at is not None


class TestRejectLeaveRequest:
    def test_sets_status_rejected(self):
        reviewer = EmployeeFactory()
        leave = LeaveRequestFactory(status=LeaveStatus.PENDING)
        updated = reject_leave_request(leave.pk, reviewed_by=reviewer, notes="Rejected.")
        assert updated.status == LeaveStatus.REJECTED
        assert updated.approval_notes == "Rejected."


class TestCancelLeaveRequest:
    def test_sets_status_cancelled(self):
        leave = LeaveRequestFactory(status=LeaveStatus.PENDING)
        updated = cancel_leave_request(leave.pk)
        assert updated.status == LeaveStatus.CANCELLED


# ---------------------------------------------------------------------------
# Work schedule service tests
# ---------------------------------------------------------------------------


class TestCreateWorkSchedule:
    def test_creates_schedule_with_default_mon_fri(self):
        emp = EmployeeFactory()
        schedule = create_work_schedule(
            employee=emp,
            expected_check_in=datetime.time(8, 0),
            expected_check_out=datetime.time(17, 0),
            effective_from=datetime.date(2026, 1, 1),
        )
        assert schedule.monday is True
        assert schedule.saturday is False
        assert schedule.sunday is False

    def test_creates_schedule_with_custom_work_days(self):
        emp = EmployeeFactory()
        schedule = create_work_schedule(
            employee=emp,
            expected_check_in=datetime.time(8, 0),
            expected_check_out=datetime.time(17, 0),
            effective_from=datetime.date(2026, 1, 1),
            work_days=frozenset({"monday", "wednesday", "friday"}),
        )
        assert schedule.monday is True
        assert schedule.tuesday is False
        assert schedule.wednesday is True
        assert schedule.friday is True
        assert schedule.saturday is False


# ---------------------------------------------------------------------------
# Selector tests
# ---------------------------------------------------------------------------


class TestSelectors:
    def test_get_attendance_record_raises_404_for_missing(self):
        import uuid

        from django.http import Http404

        with pytest.raises(Http404):
            get_attendance_record(uuid.uuid4())

    def test_get_leave_request_raises_404_for_missing(self):
        import uuid

        from django.http import Http404

        with pytest.raises(Http404):
            get_leave_request(uuid.uuid4())

    def test_get_work_schedule_raises_404_for_missing(self):
        import uuid

        from django.http import Http404

        with pytest.raises(Http404):
            get_work_schedule(uuid.uuid4())

    def test_get_active_schedule_returns_none_when_no_schedule(self):
        emp = EmployeeFactory()
        assert get_active_schedule_for_employee(emp.pk) is None

    def test_get_active_schedule_returns_default_schedule(self):
        schedule = WorkScheduleFactory(is_default=True, effective_to=None)
        result = get_active_schedule_for_employee(schedule.employee.pk)
        assert result == schedule
