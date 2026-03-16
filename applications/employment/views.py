import structlog
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from applications.employee.models import Employee
from applications.organization.models import Department, JobTitle

from .forms import ContractForm, EmploymentForm, EmploymentUpdateForm, SalaryForm
from .models import Contract, Employment, Salary
from .selectors import (
    get_contract,
    get_contracts_for_employment,
    get_employment,
    get_employment_list,
    get_salary,
    get_salary_history,
)


logger = structlog.get_logger(__name__)


# ---------------------------------------------------------------------------
# Employment views
# ---------------------------------------------------------------------------


class EmploymentListView(LoginRequiredMixin, ListView):
    template_name = "employment/employment_list.html"
    context_object_name = "employments"
    paginate_by = 25

    def get_queryset(self):
        qs = get_employment_list()
        status = self.request.GET.get("status", "").strip()
        if status:
            qs = qs.filter(status=status)
        dept = self.request.GET.get("department", "").strip()
        if dept:
            qs = qs.filter(department_id=dept)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from .constants import EmploymentStatus

        ctx["statuses"] = EmploymentStatus.choices()
        ctx["departments"] = Department.objects.order_by("name")
        ctx["selected_status"] = self.request.GET.get("status", "")
        ctx["selected_dept"] = self.request.GET.get("department", "")
        return ctx


class EmploymentDetailView(LoginRequiredMixin, DetailView):
    template_name = "employment/employment_detail.html"
    context_object_name = "employment"

    def get_object(self, queryset=None):
        return get_employment(self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["contracts"] = get_contracts_for_employment(self.object.pk)
        ctx["salary_history"] = get_salary_history(self.object.pk)
        return ctx


class EmploymentCreateView(LoginRequiredMixin, CreateView):
    model = Employment
    template_name = "employment/employment_form.html"
    form_class = EmploymentForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["employees"] = Employee.objects.order_by("last_name", "first_name")
        ctx["departments"] = Department.objects.order_by("name")
        ctx["job_titles"] = JobTitle.objects.with_department().order_by("name")
        return ctx

    def get_success_url(self):
        return reverse_lazy("employment:employment-detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form) -> HttpResponse:
        response = super().form_valid(form)
        logger.info("employment.created", employment_id=str(self.object.pk), employee=str(self.object.employee))
        messages.success(self.request, f"Employment record for \"{self.object.employee.full_name}\" created.")
        return response


class EmploymentUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "employment/employment_form.html"
    form_class = EmploymentUpdateForm

    def get_object(self, queryset=None):
        return get_employment(self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["departments"] = Department.objects.order_by("name")
        ctx["job_titles"] = JobTitle.objects.with_department().order_by("name")
        ctx["employees"] = Employee.objects.order_by("last_name", "first_name")
        return ctx

    def get_success_url(self):
        return reverse_lazy("employment:employment-detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form) -> HttpResponse:
        response = super().form_valid(form)
        logger.info("employment.updated", employment_id=str(self.object.pk))
        messages.success(self.request, "Employment record updated.")
        return response


# ---------------------------------------------------------------------------
# Contract views
# ---------------------------------------------------------------------------


class ContractCreateView(LoginRequiredMixin, CreateView):
    model = Contract
    template_name = "employment/contract_form.html"
    form_class = ContractForm

    def _get_employment(self) -> Employment:
        return get_employment(self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["employment"] = self._get_employment()
        return ctx

    def form_valid(self, form) -> HttpResponse:
        employment = self._get_employment()
        form.instance.employment = employment
        response = super().form_valid(form)
        logger.info("contract.created", contract_id=str(self.object.pk), employment_id=str(employment.pk))
        messages.success(self.request, f"\"{self.object.contract_type}\" contract created.")
        return response

    def get_success_url(self):
        return reverse_lazy("employment:employment-detail", kwargs={"pk": self.kwargs["pk"]})


class ContractUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "employment/contract_form.html"
    form_class = ContractForm

    def get_object(self, queryset=None):
        return get_contract(pk=self.kwargs["c_pk"], employment_pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["employment"] = get_employment(self.kwargs["pk"])
        return ctx

    def get_success_url(self):
        return reverse_lazy("employment:employment-detail", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form) -> HttpResponse:
        response = super().form_valid(form)
        logger.info("contract.updated", contract_id=str(self.object.pk))
        messages.success(self.request, "Contract updated.")
        return response


class ContractDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "employment/contract_confirm_delete.html"

    def get_object(self, queryset=None):
        return get_contract(pk=self.kwargs["c_pk"], employment_pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["employment"] = get_employment(self.kwargs["pk"])
        return ctx

    def get_success_url(self):
        return reverse_lazy("employment:employment-detail", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form) -> HttpResponse:
        logger.info("contract.deleted", contract_id=str(self.object.pk))
        messages.success(self.request, "Contract removed.")
        return super().form_valid(form)


# ---------------------------------------------------------------------------
# Salary views
# ---------------------------------------------------------------------------


class SalaryCreateView(LoginRequiredMixin, CreateView):
    model = Salary
    template_name = "employment/salary_form.html"
    form_class = SalaryForm

    def _get_employment(self) -> Employment:
        return get_employment(self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["employment"] = self._get_employment()
        return ctx

    def form_valid(self, form) -> HttpResponse:
        employment = self._get_employment()
        form.instance.employment = employment
        response = super().form_valid(form)
        logger.info("salary.created", salary_id=str(self.object.pk), employment_id=str(employment.pk))
        messages.success(self.request, "Salary record created.")
        return response

    def get_success_url(self):
        return reverse_lazy("employment:employment-detail", kwargs={"pk": self.kwargs["pk"]})


class SalaryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "employment/salary_form.html"
    form_class = SalaryForm

    def get_object(self, queryset=None):
        return get_salary(pk=self.kwargs["s_pk"], employment_pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["employment"] = get_employment(self.kwargs["pk"])
        return ctx

    def get_success_url(self):
        return reverse_lazy("employment:employment-detail", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form) -> HttpResponse:
        response = super().form_valid(form)
        logger.info("salary.updated", salary_id=str(self.object.pk))
        messages.success(self.request, "Salary record updated.")
        return response


class SalaryDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "employment/salary_confirm_delete.html"

    def get_object(self, queryset=None):
        return get_salary(pk=self.kwargs["s_pk"], employment_pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["employment"] = get_employment(self.kwargs["pk"])
        return ctx

    def get_success_url(self):
        return reverse_lazy("employment:employment-detail", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form) -> HttpResponse:
        logger.info("salary.deleted", salary_id=str(self.object.pk))
        messages.success(self.request, "Salary record removed.")
        return super().form_valid(form)
