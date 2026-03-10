from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from shared.base_models import BaseModel

from .constants import FileType, ImportLogStatus, ImportStatus, ImportType
from .managers import ImportJobManager


class ImportJob(BaseModel):
    """Represents a single bulk-import session uploaded by a HR admin."""

    import_type = models.CharField(
        _("import type"),
        max_length=30,
        choices=ImportType.choices(),
    )
    status = models.CharField(
        _("status"),
        max_length=20,
        choices=ImportStatus.choices(),
        default=ImportStatus.PENDING,
        db_index=True,
    )
    file = models.FileField(
        _("file"),
        upload_to="imports/",
    )
    file_name = models.CharField(_("original file name"), max_length=255)
    file_type = models.CharField(
        _("file type"),
        max_length=10,
        choices=FileType.choices(),
    )

    # Row counters
    total_rows = models.PositiveIntegerField(_("total rows"), default=0)
    processed_rows = models.PositiveIntegerField(_("processed rows"), default=0)
    success_rows = models.PositiveIntegerField(_("success rows"), default=0)
    failed_rows = models.PositiveIntegerField(_("failed rows"), default=0)

    # Field mapping: { "csv_column_header": "model_field_name" }
    field_mapping = models.JSONField(_("field mapping"), null=True, blank=True)

    # High-level error summary (e.g. validation failures per field)
    error_summary = models.TextField(_("error summary"), blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="import_jobs",
        verbose_name=_("created by"),
    )

    objects = ImportJobManager()

    class Meta:
        verbose_name = _("Import Job")
        verbose_name_plural = _("Import Jobs")
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.import_type} import — {self.file_name} ({self.status})"

    @property
    def progress_percent(self) -> int:
        if self.total_rows == 0:
            return 0
        return int((self.processed_rows / self.total_rows) * 100)

    @property
    def is_editable(self) -> bool:
        """True when the mapping can still be configured."""
        return self.status in (ImportStatus.PENDING, ImportStatus.MAPPING)


class ImportLog(BaseModel):
    """Row-level result for a single record within an ImportJob."""

    job = models.ForeignKey(
        ImportJob,
        on_delete=models.CASCADE,
        related_name="logs",
        verbose_name=_("import job"),
    )
    row_number = models.PositiveIntegerField(_("row number"))
    status = models.CharField(
        _("status"),
        max_length=10,
        choices=ImportLogStatus.choices(),
        db_index=True,
    )
    raw_data = models.JSONField(_("raw data"))
    error_message = models.TextField(_("error message"), blank=True)

    class Meta:
        verbose_name = _("Import Log")
        verbose_name_plural = _("Import Logs")
        ordering = ("row_number",)

    def __str__(self) -> str:
        return f"Row {self.row_number} — {self.status}"
