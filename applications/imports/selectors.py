from __future__ import annotations

from django.db.models import QuerySet

from .models import ImportJob, ImportLog


def get_import_job_list() -> QuerySet[ImportJob]:
    return ImportJob.objects.select_related("created_by").order_by("-created_at")


def get_import_job(pk: str) -> ImportJob:
    return ImportJob.objects.select_related("created_by").get(pk=pk)


def get_import_logs(job: ImportJob) -> QuerySet[ImportLog]:
    return ImportLog.objects.filter(job=job).order_by("row_number")


def get_error_logs(job: ImportJob) -> QuerySet[ImportLog]:
    from .constants import ImportLogStatus  # noqa: PLC0415

    return ImportLog.objects.filter(job=job, status=ImportLogStatus.ERROR).order_by("row_number")
