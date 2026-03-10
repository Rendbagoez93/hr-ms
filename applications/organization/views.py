import structlog
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import Department, JobTitle
from .selectors import get_department, get_department_list, get_jobtitle, get_jobtitle_list


logger = structlog.get_logger(__name__)

_HTMX_HEADER = "HX-Request"


# ---------------------------------------------------------------------------
# Department views
# ---------------------------------------------------------------------------


class DepartmentListView(LoginRequiredMixin, ListView):
    template_name = "organization/department_list.html"
    context_object_name = "departments"
    paginate_by = 20

    def get_queryset(self):
        return get_department_list()


class DepartmentDetailView(LoginRequiredMixin, DetailView):
    template_name = "organization/department_detail.html"
    context_object_name = "department"

    def get_object(self, queryset=None):
        return get_department(self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["job_titles"] = self.object.job_titles.select_related("department").order_by("name")
        ctx["children"] = self.object.children.order_by("name")
        return ctx


class DepartmentCreateView(LoginRequiredMixin, CreateView):
    model = Department
    template_name = "organization/department_form.html"
    fields = ["name", "code", "description", "parent"]
    success_url = reverse_lazy("organization:department-list")

    def form_valid(self, form) -> HttpResponse:
        response = super().form_valid(form)
        logger.info("department.created", department_id=str(self.object.pk), name=self.object.name)
        messages.success(self.request, f"Department \"{self.object.name}\" created successfully.")
        return response


class DepartmentUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "organization/department_form.html"
    fields = ["name", "code", "description", "parent"]

    def get_object(self, queryset=None):
        return get_department(self.kwargs["pk"])

    def get_success_url(self):
        return reverse_lazy("organization:department-detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form) -> HttpResponse:
        response = super().form_valid(form)
        logger.info("department.updated", department_id=str(self.object.pk), name=self.object.name)
        messages.success(self.request, f"Department \"{self.object.name}\" updated.")
        return response


class DepartmentDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "organization/department_confirm_delete.html"
    success_url = reverse_lazy("organization:department-list")

    def get_object(self, queryset=None):
        return get_department(self.kwargs["pk"])

    def form_valid(self, form) -> HttpResponse:
        logger.info("department.deleted", department_id=str(self.object.pk), name=self.object.name)
        messages.success(self.request, f"Department \"{self.object.name}\" deleted.")
        return super().form_valid(form)


# ---------------------------------------------------------------------------
# JobTitle views
# ---------------------------------------------------------------------------


class JobTitleListView(LoginRequiredMixin, ListView):
    template_name = "organization/jobtitle_list.html"
    context_object_name = "job_titles"
    paginate_by = 20

    def get_queryset(self):
        qs = get_jobtitle_list()
        dept = self.request.GET.get("department")
        if dept:
            qs = qs.filter(department_id=dept)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["departments"] = Department.objects.order_by("name")
        ctx["selected_dept"] = self.request.GET.get("department", "")
        return ctx


class JobTitleCreateView(LoginRequiredMixin, CreateView):
    model = JobTitle
    template_name = "organization/jobtitle_form.html"
    fields = ["name", "code", "description", "department"]
    success_url = reverse_lazy("organization:jobtitle-list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["departments"] = Department.objects.order_by("name")
        return ctx

    def form_valid(self, form) -> HttpResponse:
        response = super().form_valid(form)
        logger.info("jobtitle.created", jobtitle_id=str(self.object.pk), name=self.object.name)
        messages.success(self.request, f"Job title \"{self.object.name}\" created successfully.")
        return response


class JobTitleUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "organization/jobtitle_form.html"
    fields = ["name", "code", "description", "department"]
    success_url = reverse_lazy("organization:jobtitle-list")

    def get_object(self, queryset=None):
        return get_jobtitle(self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["departments"] = Department.objects.order_by("name")
        return ctx

    def form_valid(self, form) -> HttpResponse:
        response = super().form_valid(form)
        logger.info("jobtitle.updated", jobtitle_id=str(self.object.pk), name=self.object.name)
        messages.success(self.request, f"Job title \"{self.object.name}\" updated.")
        return response


class JobTitleDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "organization/jobtitle_confirm_delete.html"
    success_url = reverse_lazy("organization:jobtitle-list")

    def get_object(self, queryset=None):
        return get_jobtitle(self.kwargs["pk"])

    def form_valid(self, form) -> HttpResponse:
        logger.info("jobtitle.deleted", jobtitle_id=str(self.object.pk), name=self.object.name)
        messages.success(self.request, f"Job title \"{self.object.name}\" deleted.")
        return super().form_valid(form)
