from __future__ import annotations

import datetime
import decimal

import structlog
from django.utils import timezone

from .models import AttendanceRecord, LeaveRequest, WorkSchedule
from .selectors import get_attendance_record, get_leave_request, get_work_schedule


logger = structlog.get_logger(__name__)

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_SECONDS_PER_HOUR = decimal.Decimal(3600)
_HOUR_PLACES = decimal.Decimal("0.01")


def _compute_work_hours(
    check_in: datetime.time | None,
    check_out: datetime.time | None,
) -> decimal.Decimal | None:
    """Return worked hours as a Decimal, or None if either time is missing."""
    if not check_in or not check_out:
        return None
    today = datetime.date.today()
    delta = datetime.datetime.combine(today, check_out) - datetime.datetime.combine(today, check_in)
    hours = decimal.Decimal(delta.total_seconds()) / _SECONDS_PER_HOUR
    return hours.quantize(_HOUR_PLACES)


# ---------------------------------------------------------------------------
# Attendance record services
# ---------------------------------------------------------------------------


def create_attendance_record(
    *,
    employee,
    date: datetime.date,
    status: str,
    check_in: datetime.time | None = None,
    check_out: datetime.time | None = None,
    late_minutes: int = 0,
    notes: str = "",
) -> AttendanceRecord:
    record = AttendanceRecord(
        employee=employee,
        date=date,
        status=status,
        check_in=check_in,
        check_out=check_out,
        work_hours=_compute_work_hours(check_in, check_out),
        late_minutes=late_minutes,
        notes=notes,
    )
    record.full_clean()
    record.save()
    logger.info("attendance_record_created", record_id=str(record.pk), employee_id=str(employee.pk), date=str(date))
    return record


def update_attendance_record(  # noqa: PLR0913
    pk,
    *,
    status: str | None = None,
    check_in: datetime.time | None = None,
    check_out: datetime.time | None = None,
    late_minutes: int | None = None,
    notes: str | None = None,
) -> AttendanceRecord:
    record = get_attendance_record(pk)
    if status is not None:
        record.status = status
    if check_in is not None:
        record.check_in = check_in
    if check_out is not None:
        record.check_out = check_out
    if late_minutes is not None:
        record.late_minutes = late_minutes
    if notes is not None:
        record.notes = notes
    record.work_hours = _compute_work_hours(record.check_in, record.check_out)
    record.full_clean()
    record.save()
    logger.info("attendance_record_updated", record_id=str(record.pk))
    return record


def delete_attendance_record(pk) -> None:
    record = get_attendance_record(pk)
    record.delete()
    logger.info("attendance_record_deleted", record_id=str(pk))


# ---------------------------------------------------------------------------
# Leave request services
# ---------------------------------------------------------------------------


def create_leave_request(
    *,
    employee,
    leave_type: str,
    start_date: datetime.date,
    end_date: datetime.date,
    reason: str,
) -> LeaveRequest:
    total_days = (end_date - start_date).days + 1
    leave = LeaveRequest(
        employee=employee,
        leave_type=leave_type,
        start_date=start_date,
        end_date=end_date,
        total_days=total_days,
        reason=reason,
    )
    leave.full_clean()
    leave.save()
    logger.info("leave_request_created", leave_id=str(leave.pk), employee_id=str(employee.pk))
    return leave


def approve_leave_request(pk, *, reviewed_by, notes: str = "") -> LeaveRequest:
    from .constants import LeaveStatus

    leave = get_leave_request(pk)
    leave.status = LeaveStatus.APPROVED
    leave.approved_by = reviewed_by
    leave.approval_notes = notes
    leave.reviewed_at = timezone.now()
    leave.full_clean()
    leave.save()
    logger.info("leave_request_approved", leave_id=str(leave.pk), reviewed_by=str(reviewed_by.pk))
    return leave


def reject_leave_request(pk, *, reviewed_by, notes: str = "") -> LeaveRequest:
    from .constants import LeaveStatus

    leave = get_leave_request(pk)
    leave.status = LeaveStatus.REJECTED
    leave.approved_by = reviewed_by
    leave.approval_notes = notes
    leave.reviewed_at = timezone.now()
    leave.full_clean()
    leave.save()
    logger.info("leave_request_rejected", leave_id=str(leave.pk), reviewed_by=str(reviewed_by.pk))
    return leave


def cancel_leave_request(pk) -> LeaveRequest:
    from .constants import LeaveStatus

    leave = get_leave_request(pk)
    leave.status = LeaveStatus.CANCELLED
    leave.full_clean()
    leave.save()
    logger.info("leave_request_cancelled", leave_id=str(leave.pk))
    return leave


# ---------------------------------------------------------------------------
# Work schedule services
# ---------------------------------------------------------------------------

_WORK_DAY_FIELDS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
_DEFAULT_WORK_DAYS: frozenset[str] = frozenset({"monday", "tuesday", "wednesday", "thursday", "friday"})


def create_work_schedule(
    *,
    employee,
    expected_check_in: datetime.time,
    expected_check_out: datetime.time,
    effective_from: datetime.date,
    name: str = "Standard",
    work_days: frozenset[str] | None = None,
    effective_to: datetime.date | None = None,
) -> WorkSchedule:
    days = work_days if work_days is not None else _DEFAULT_WORK_DAYS
    schedule = WorkSchedule(
        employee=employee,
        name=name,
        expected_check_in=expected_check_in,
        expected_check_out=expected_check_out,
        effective_from=effective_from,
        effective_to=effective_to,
        **{day: day in days for day in _WORK_DAY_FIELDS},
    )
    schedule.full_clean()
    schedule.save()
    logger.info("work_schedule_created", schedule_id=str(schedule.pk), employee_id=str(employee.pk))
    return schedule


def update_work_schedule(  # noqa: PLR0913
    pk,
    *,
    name: str | None = None,
    expected_check_in: datetime.time | None = None,
    expected_check_out: datetime.time | None = None,
    effective_to: datetime.date | None = None,
    work_days: frozenset[str] | None = None,
    is_default: bool | None = None,
) -> WorkSchedule:
    schedule = get_work_schedule(pk)
    if name is not None:
        schedule.name = name
    if expected_check_in is not None:
        schedule.expected_check_in = expected_check_in
    if expected_check_out is not None:
        schedule.expected_check_out = expected_check_out
    if effective_to is not None:
        schedule.effective_to = effective_to
    if work_days is not None:
        for day in _WORK_DAY_FIELDS:
            setattr(schedule, day, day in work_days)
    if is_default is not None:
        schedule.is_default = is_default
    schedule.full_clean()
    schedule.save()
    logger.info("work_schedule_updated", schedule_id=str(schedule.pk))
    return schedule
