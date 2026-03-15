from __future__ import annotations

import datetime

from django.db import models
from django.utils import timezone


class WorkScheduleQuerySet(models.QuerySet):
    def for_employee(self, employee_pk) -> "WorkScheduleQuerySet":
        return self.filter(employee_id=employee_pk)

    def active(self) -> "WorkScheduleQuerySet":
        """Schedules currently in effect: no end date, or end date in the future."""
        today = timezone.now().date()
        return self.filter(
            models.Q(effective_to__isnull=True) | models.Q(effective_to__gte=today)
        )

    def default(self) -> "WorkScheduleQuerySet":
        return self.filter(is_default=True)

    def with_employee(self) -> "WorkScheduleQuerySet":
        return self.select_related("employee")


class WorkScheduleManager(models.Manager.from_queryset(WorkScheduleQuerySet)):
    def get_queryset(self) -> WorkScheduleQuerySet:
        return super().get_queryset().filter(deleted_at__isnull=True)


class AttendanceRecordQuerySet(models.QuerySet):
    def for_employee(self, employee_pk) -> "AttendanceRecordQuerySet":
        return self.filter(employee_id=employee_pk)

    def for_date_range(self, start: datetime.date, end: datetime.date) -> "AttendanceRecordQuerySet":
        return self.filter(date__gte=start, date__lte=end)

    def for_month(self, year: int, month: int) -> "AttendanceRecordQuerySet":
        return self.filter(date__year=year, date__month=month)

    def present(self) -> "AttendanceRecordQuerySet":
        from .constants import AttendanceStatus

        return self.filter(status__in=AttendanceStatus.present_statuses())

    def absent(self) -> "AttendanceRecordQuerySet":
        from .constants import AttendanceStatus

        return self.filter(status__in=AttendanceStatus.absent_statuses())

    def with_employee(self) -> "AttendanceRecordQuerySet":
        return self.select_related("employee__user")


class AttendanceRecordManager(models.Manager.from_queryset(AttendanceRecordQuerySet)):
    def get_queryset(self) -> AttendanceRecordQuerySet:
        return super().get_queryset().filter(deleted_at__isnull=True)


class LeaveRequestQuerySet(models.QuerySet):
    def for_employee(self, employee_pk) -> "LeaveRequestQuerySet":
        return self.filter(employee_id=employee_pk)

    def pending(self) -> "LeaveRequestQuerySet":
        from .constants import LeaveStatus

        return self.filter(status=LeaveStatus.PENDING)

    def approved(self) -> "LeaveRequestQuerySet":
        from .constants import LeaveStatus

        return self.filter(status=LeaveStatus.APPROVED)

    def for_date_range(self, start: datetime.date, end: datetime.date) -> "LeaveRequestQuerySet":
        """Leave requests that overlap the given date range."""
        return self.filter(start_date__lte=end, end_date__gte=start)

    def with_employee(self) -> "LeaveRequestQuerySet":
        return self.select_related("employee__user", "approved_by")


class LeaveRequestManager(models.Manager.from_queryset(LeaveRequestQuerySet)):
    def get_queryset(self) -> LeaveRequestQuerySet:
        return super().get_queryset().filter(deleted_at__isnull=True)
