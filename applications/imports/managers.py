from __future__ import annotations

from django.db import models

from .constants import ImportStatus


class ImportJobQuerySet(models.QuerySet):
    def pending(self) -> ImportJobQuerySet:
        return self.filter(status=ImportStatus.PENDING)

    def completed(self) -> ImportJobQuerySet:
        return self.filter(status=ImportStatus.COMPLETED)

    def recent(self) -> ImportJobQuerySet:
        return self.order_by("-created_at")


class ImportJobManager(models.Manager.from_queryset(ImportJobQuerySet)):
    pass
