from __future__ import annotations

from django.db import models


class DepartmentQuerySet(models.QuerySet):
    def active(self) -> "DepartmentQuerySet":
        return self.filter(is_active=True)

    def root(self) -> "DepartmentQuerySet":
        """Return top-level departments with no parent."""
        return self.filter(parent__isnull=True)

    def with_children(self) -> "DepartmentQuerySet":
        return self.prefetch_related("children")


class DepartmentManager(models.Manager.from_queryset(DepartmentQuerySet)):
    def get_queryset(self) -> DepartmentQuerySet:
        return super().get_queryset().filter(deleted_at__isnull=True)


class JobTitleQuerySet(models.QuerySet):
    def active(self) -> "JobTitleQuerySet":
        return self.filter(is_active=True)

    def for_department(self, department_id) -> "JobTitleQuerySet":
        return self.filter(department_id=department_id)

    def with_department(self) -> "JobTitleQuerySet":
        return self.select_related("department")


class JobTitleManager(models.Manager.from_queryset(JobTitleQuerySet)):
    def get_queryset(self) -> JobTitleQuerySet:
        return super().get_queryset().filter(deleted_at__isnull=True)
