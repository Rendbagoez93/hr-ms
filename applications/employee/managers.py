from __future__ import annotations

from django.db import models


class EmployeeQuerySet(models.QuerySet):
    def active(self) -> "EmployeeQuerySet":
        return self.filter(is_active=True)

    def with_employment(self) -> "EmployeeQuerySet":
        return self.select_related("employment__department", "employment__job_title")

    def with_emergency_contacts(self) -> "EmployeeQuerySet":
        return self.prefetch_related("emergency_contacts")

    def with_user(self) -> "EmployeeQuerySet":
        return self.select_related("user")


class EmployeeManager(models.Manager):
    def get_queryset(self) -> EmployeeQuerySet:
        return EmployeeQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)
