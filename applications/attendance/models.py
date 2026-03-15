from django.db import models
from django.utils.translation import gettext_lazy as _

from applications.employee.models import Employee
from shared.base_models import BaseModel

from .constants import AttendanceStatus, LeaveStatus, LeaveType
from .managers import AttendanceRecordManager, LeaveRequestManager, WorkScheduleManager


class WorkSchedule(BaseModel):
    """Defines expected working hours and days for an employee."""

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="work_schedules",
        verbose_name=_("employee"),
    )
    name = models.CharField(_("schedule name"), max_length=100, default="Standard")
    is_default = models.BooleanField(_("default schedule"), default=False)

    # Work days
    monday = models.BooleanField(_("Monday"), default=True)
    tuesday = models.BooleanField(_("Tuesday"), default=True)
    wednesday = models.BooleanField(_("Wednesday"), default=True)
    thursday = models.BooleanField(_("Thursday"), default=True)
    friday = models.BooleanField(_("Friday"), default=True)
    saturday = models.BooleanField(_("Saturday"), default=False)
    sunday = models.BooleanField(_("Sunday"), default=False)

    # Expected clock-in / clock-out times
    expected_check_in = models.TimeField(_("expected check-in"))
    expected_check_out = models.TimeField(_("expected check-out"))

    # Validity window
    effective_from = models.DateField(_("effective from"))
    effective_to = models.DateField(_("effective to"), null=True, blank=True)

    objects = WorkScheduleManager()

    class Meta:
        verbose_name = _("Work Schedule")
        verbose_name_plural = _("Work Schedules")
        ordering = ("-effective_from",)

    def __str__(self) -> str:
        return f"{self.employee} — {self.name} (from {self.effective_from})"

    @property
    def is_open_ended(self) -> bool:
        """True when this schedule has no expiry date."""
        return self.effective_to is None

    @property
    def work_days(self) -> list[str]:
        """Return a list of day names that are enabled on this schedule."""
        day_names = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        return [day for day in day_names if getattr(self, day)]


class AttendanceRecord(BaseModel):
    """Daily attendance record for a single employee."""

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="attendance_records",
        verbose_name=_("employee"),
    )
    date = models.DateField(_("date"))
    status = models.CharField(
        _("status"),
        max_length=30,
        choices=AttendanceStatus.choices(),
        default=AttendanceStatus.PRESENT,
    )
    check_in = models.TimeField(_("check-in time"), null=True, blank=True)
    check_out = models.TimeField(_("check-out time"), null=True, blank=True)
    work_hours = models.DecimalField(
        _("work hours"),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Total hours worked for the day, computed from check-in / check-out."),
    )
    late_minutes = models.PositiveIntegerField(
        _("late minutes"),
        default=0,
        help_text=_("Minutes the employee arrived after the scheduled check-in time."),
    )
    notes = models.TextField(_("notes"), blank=True)

    objects = AttendanceRecordManager()

    class Meta:
        verbose_name = _("Attendance Record")
        verbose_name_plural = _("Attendance Records")
        ordering = ("-date",)
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "date"],
                name="unique_employee_date_attendance",
            )
        ]

    def __str__(self) -> str:
        return f"{self.employee} – {self.date} ({self.status})"


class LeaveRequest(BaseModel):
    """Employee request for a period of leave or absence."""

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="leave_requests",
        verbose_name=_("employee"),
    )
    leave_type = models.CharField(
        _("leave type"),
        max_length=20,
        choices=LeaveType.choices(),
    )
    start_date = models.DateField(_("start date"))
    end_date = models.DateField(_("end date"))
    total_days = models.PositiveSmallIntegerField(
        _("total days"),
        help_text=_("Number of calendar days covered by this request."),
    )
    reason = models.TextField(_("reason"))
    status = models.CharField(
        _("status"),
        max_length=20,
        choices=LeaveStatus.choices(),
        default=LeaveStatus.PENDING,
    )
    approved_by = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_leave_requests",
        verbose_name=_("reviewed by"),
    )
    approval_notes = models.TextField(_("approval notes"), blank=True)
    reviewed_at = models.DateTimeField(_("reviewed at"), null=True, blank=True)

    objects = LeaveRequestManager()

    class Meta:
        verbose_name = _("Leave Request")
        verbose_name_plural = _("Leave Requests")
        ordering = ("-start_date",)

    def __str__(self) -> str:
        return f"{self.employee} — {self.leave_type} ({self.start_date} → {self.end_date})"

    @property
    def is_pending(self) -> bool:
        return self.status == LeaveStatus.PENDING

    @property
    def is_approved(self) -> bool:
        return self.status == LeaveStatus.APPROVED
