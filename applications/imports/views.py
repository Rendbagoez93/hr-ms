from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, View
import structlog

from .constants import IMPORT_FIELD_DEFINITIONS, FileType, ImportStatus, ImportType
from .models import ImportJob
from .selectors import get_error_logs, get_import_job, get_import_job_list, get_import_logs
from .services import detect_field_mapping, process_import_job, read_file_headers


logger = structlog.get_logger(__name__)


class ImportJobListView(LoginRequiredMixin, ListView):
    template_name = "settings/bulk_import_list.html"
    context_object_name = "jobs"
    paginate_by = 20

    def get_queryset(self):
        return get_import_job_list()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["import_types"] = ImportType.choices()
        ctx["active_group"] = "settings"
        ctx["breadcrumbs"] = [
            {"label": "Settings", "url": reverse("settings:index")},
            {"label": "Bulk Import", "url": None},
        ]
        return ctx


class ImportJobCreateView(LoginRequiredMixin, View):
    template_name = "settings/bulk_import_create.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        return self._render(request)

    def post(self, request: HttpRequest) -> HttpResponse:
        import_type = request.POST.get("import_type", "").strip()
        uploaded_file = request.FILES.get("file")

        if not import_type or import_type not in [t.value for t in ImportType]:
            messages.error(request, "Please select a valid import type.")
            return self._render(request)

        if not uploaded_file:
            messages.error(request, "Please upload a file.")
            return self._render(request)

        filename = uploaded_file.name.lower()
        if filename.endswith(".csv"):
            file_type = FileType.CSV
        elif filename.endswith((".xlsx", ".xls")):
            file_type = FileType.XLSX
        else:
            messages.error(request, "Only CSV (.csv) or Excel (.xlsx) files are supported.")
            return self._render(request)

        job = ImportJob.objects.create(
            import_type=import_type,
            file=uploaded_file,
            file_name=uploaded_file.name,
            file_type=file_type,
            status=ImportStatus.MAPPING,
            created_by=request.user,
        )

        logger.info("Import job created", job_id=str(job.pk), import_type=import_type, user=request.user.pk)
        return redirect(reverse("imports:mapping", kwargs={"pk": job.pk}))

    def _render(self, request: HttpRequest) -> HttpResponse:
        from django.shortcuts import render  # noqa: PLC0415

        return render(
            request,
            self.template_name,
            {
                "import_types": ImportType.choices(),
                "active_group": "settings",
                "breadcrumbs": [
                    {"label": "Settings", "url": reverse("settings:index")},
                    {"label": "Bulk Import", "url": reverse("imports:list")},
                    {"label": "New Import", "url": None},
                ],
            },
        )


class ImportJobMappingView(LoginRequiredMixin, View):
    template_name = "settings/bulk_import_mapping.html"

    def get(self, request: HttpRequest, pk: str) -> HttpResponse:
        job = get_object_or_404(ImportJob, pk=pk)
        headers, suggested_mapping = self._load_mapping(job)
        field_defs = IMPORT_FIELD_DEFINITIONS.get(job.import_type, {})
        return self._render(request, job, headers, suggested_mapping, field_defs)

    def post(self, request: HttpRequest, pk: str) -> HttpResponse:
        job = get_object_or_404(ImportJob, pk=pk)
        if not job.is_editable:
            messages.warning(request, "This import job cannot be modified.")
            return redirect(reverse("imports:detail", kwargs={"pk": pk}))

        headers, _ = self._load_mapping(job)
        mapping: dict[str, str | None] = {}
        for header in headers:
            field = request.POST.get(f"mapping_{header}", "").strip() or None
            mapping[header] = field

        job.field_mapping = mapping
        job.status = ImportStatus.READY
        job.save(update_fields=["field_mapping", "status"])

        messages.success(request, "Field mapping saved. You can now run the import.")
        return redirect(reverse("imports:detail", kwargs={"pk": pk}))

    def _load_mapping(self, job: ImportJob) -> tuple[list[str], dict[str, str | None]]:
        job.file.open("rb")
        try:
            headers = read_file_headers(job.file, job.file_type)
        finally:
            job.file.close()

        if job.field_mapping:
            return headers, job.field_mapping

        return headers, detect_field_mapping(headers, job.import_type)

    def _render(self, request, job, headers, mapping, field_defs) -> HttpResponse:
        from django.shortcuts import render  # noqa: PLC0415

        return render(
            request,
            self.template_name,
            {
                "job": job,
                "headers": headers,
                "mapping": mapping,
                "field_defs": field_defs,
                "active_group": "settings",
                "breadcrumbs": [
                    {"label": "Settings", "url": reverse("settings:index")},
                    {"label": "Bulk Import", "url": reverse("imports:list")},
                    {"label": "Field Mapping", "url": None},
                ],
            },
        )


class ImportJobProcessView(LoginRequiredMixin, View):
    """Trigger the actual row-by-row import processing."""

    def post(self, request: HttpRequest, pk: str) -> HttpResponse:
        job = get_object_or_404(ImportJob, pk=pk)

        if job.status not in (ImportStatus.READY, ImportStatus.MAPPING):
            messages.warning(request, "This job cannot be re-processed.")
            return redirect(reverse("imports:detail", kwargs={"pk": pk}))

        if not job.field_mapping:
            messages.error(request, "Please configure field mapping before running the import.")
            return redirect(reverse("imports:mapping", kwargs={"pk": pk}))

        process_import_job(str(job.pk))
        job.refresh_from_db()

        if job.status == ImportStatus.COMPLETED:
            messages.success(request, f"Import completed: {job.success_rows} records imported.")
        elif job.status == ImportStatus.PARTIAL:
            messages.warning(
                request,
                f"Import partially completed: {job.success_rows} succeeded, {job.failed_rows} failed.",
            )
        else:
            messages.error(request, f"Import failed. {job.failed_rows} rows had errors.")

        return redirect(reverse("imports:detail", kwargs={"pk": pk}))


class ImportJobDetailView(LoginRequiredMixin, DetailView):
    template_name = "settings/bulk_import_detail.html"
    context_object_name = "job"

    def get_object(self, queryset=None):  # noqa: ARG002
        return get_import_job(self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        job = self.object
        ctx["logs"] = get_import_logs(job)
        ctx["error_logs"] = get_error_logs(job)
        ctx["active_group"] = "settings"
        ctx["breadcrumbs"] = [
            {"label": "Settings", "url": reverse("settings:index")},
            {"label": "Bulk Import", "url": reverse("imports:list")},
            {"label": job.file_name, "url": None},
        ]
        return ctx
