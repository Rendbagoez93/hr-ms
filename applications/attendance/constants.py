from enum import StrEnum


class AttendanceStatus(StrEnum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    HALF_DAY = "half_day"
    ON_LEAVE = "on_leave"
    HOLIDAY = "holiday"
    WEEKEND = "weekend"

    @classmethod
    def choices(cls):
        return [(s.value, s.name.replace("_", " ").title()) for s in cls]

    @classmethod
    def present_statuses(cls) -> list[str]:
        """Statuses that count as attendance for payroll/reporting."""
        return [cls.PRESENT, cls.LATE, cls.HALF_DAY]

    @classmethod
    def absent_statuses(cls) -> list[str]:
        """Statuses that represent non-attendance days."""
        return [cls.ABSENT, cls.ON_LEAVE, cls.HOLIDAY, cls.WEEKEND]


class LeaveType(StrEnum):
    ANNUAL = "annual"
    SICK = "sick"
    PERSONAL = "personal"
    MATERNITY = "maternity"
    PATERNITY = "paternity"
    UNPAID = "unpaid"
    OTHER = "other"

    @classmethod
    def choices(cls):
        return [(lt.value, lt.name.replace("_", " ").title()) for lt in cls]

    @classmethod
    def paid_types(cls) -> list[str]:
        """Leave types that are paid."""
        return [cls.ANNUAL, cls.SICK, cls.PERSONAL, cls.MATERNITY, cls.PATERNITY]


class LeaveStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

    @classmethod
    def choices(cls):
        return [(ls.value, ls.name.replace("_", " ").title()) for ls in cls]

    @classmethod
    def terminal_statuses(cls) -> list[str]:
        """Statuses from which the request can no longer be modified."""
        return [cls.APPROVED, cls.REJECTED, cls.CANCELLED]
