from __future__ import annotations

from django.db import models
from django.utils import timezone

from .constants import EmploymentStatus


class EmploymentQuerySet(models.QuerySet):
    def active(self) -> EmploymentQuerySet:
        return self.filter(status__in=EmploymentStatus.active_statuses())

    def with_employee(self) -> EmploymentQuerySet:
        return self.select_related("employee")

    def with_position(self) -> EmploymentQuerySet:
        return self.select_related("department", "job_title")

    def with_reporting_manager(self) -> EmploymentQuerySet:
        return self.select_related("reporting_manager")

    def with_full_detail(self) -> EmploymentQuerySet:
        return self.select_related("employee", "department", "job_title", "reporting_manager")


class EmploymentManager(models.Manager):
    def get_queryset(self) -> EmploymentQuerySet:
        return EmploymentQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)


class ContractQuerySet(models.QuerySet):
    def current(self) -> ContractQuerySet:
        """Contracts with no end date (open-ended) or end date in the future."""
        return self.filter(models.Q(end_date__isnull=True) | models.Q(end_date__gte=timezone.now().date()))


class ContractManager(models.Manager):
    def get_queryset(self) -> ContractQuerySet:
        return ContractQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)


class SalaryQuerySet(models.QuerySet):
    def current(self) -> SalaryQuerySet:
        """Salary records with no end date — the currently active rate."""
        return self.filter(end_date__isnull=True)

    def history(self) -> SalaryQuerySet:
        """All past salary records that have been superseded."""
        return self.filter(end_date__isnull=False)


class SalaryManager(models.Manager):
    def get_queryset(self) -> SalaryQuerySet:
        return SalaryQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)
