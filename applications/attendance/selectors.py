from __future__ import annotations

import datetime

from django.shortcuts import get_object_or_404

from .models import AttendanceRecord, LeaveRequest, WorkSchedule


# ---------------------------------------------------------------------------
# Attendance record selectors
# ---------------------------------------------------------------------------


def get_attendance_list(
    employee_pk=None,
    date_range: tuple[datetime.date, datetime.date] | None = None,
):
    qs = AttendanceRecord.objects.with_employee().order_by("-date")
    if employee_pk:
        qs = qs.for_employee(employee_pk)
    if date_range:
        qs = qs.for_date_range(*date_range)
    return qs


def get_attendance_record(pk) -> AttendanceRecord:
    return get_object_or_404(AttendanceRecord.objects.with_employee(), pk=pk)


# ---------------------------------------------------------------------------
# Leave request selectors
# ---------------------------------------------------------------------------


def get_leave_request_list(employee_pk=None, status: str | None = None):
    qs = LeaveRequest.objects.with_employee().order_by("-start_date")
    if employee_pk:
        qs = qs.for_employee(employee_pk)
    if status:
        qs = qs.filter(status=status)
    return qs


def get_leave_request(pk) -> LeaveRequest:
    return get_object_or_404(LeaveRequest.objects.with_employee(), pk=pk)


# ---------------------------------------------------------------------------
# Work schedule selectors
# ---------------------------------------------------------------------------


def get_work_schedule_list(employee_pk=None, active_only: bool = False):
    qs = WorkSchedule.objects.with_employee().order_by("-effective_from")
    if employee_pk:
        qs = qs.for_employee(employee_pk)
    if active_only:
        qs = qs.active()
    return qs


def get_work_schedule(pk) -> WorkSchedule:
    return get_object_or_404(WorkSchedule.objects.with_employee(), pk=pk)


def get_active_schedule_for_employee(employee_pk) -> WorkSchedule | None:
    """Return the current default work schedule for an employee, or None."""
    return WorkSchedule.objects.for_employee(employee_pk).active().default().first()
