from enum import StrEnum


class EmploymentStatus(StrEnum):
    ACTIVE = "active"
    PROBATION = "probation"
    ON_LEAVE = "on_leave"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"
    RESIGNED = "resigned"

    @classmethod
    def choices(cls):
        return [(s.value, s.name.replace("_", " ").title()) for s in cls]

    @classmethod
    def active_statuses(cls) -> list[str]:
        """Statuses that represent a currently working employee."""
        return [cls.ACTIVE, cls.PROBATION, cls.ON_LEAVE]


class ContractType(StrEnum):
    PERMANENT = "permanent"
    FIXED_TERM = "fixed_term"
    PROBATIONARY = "probationary"
    INTERNSHIP = "internship"
    PART_TIME = "part_time"
    FREELANCE = "freelance"

    @classmethod
    def choices(cls):
        return [(c.value, c.name.replace("_", " ").title()) for c in cls]


class PaymentFrequency(StrEnum):
    WEEKLY = "weekly"
    BI_WEEKLY = "bi_weekly"
    MONTHLY = "monthly"
    ANNUAL = "annual"

    @classmethod
    def choices(cls):
        return [(f.value, f.name.replace("_", " ").title()) for f in cls]


class WorkLocationType(StrEnum):
    ONSITE = "onsite"
    REMOTE = "remote"
    HYBRID = "hybrid"

    @classmethod
    def choices(cls):
        return [(loc.value, loc.name.replace("_", " ").title()) for loc in cls]
