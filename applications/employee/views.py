import structlog
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from applications.organization.models import Department, JobTitle

from .models import EmergencyContact, Employee
from .selectors import (
    get_emergency_contact,
    get_emergency_contacts_for_employee,
    get_employee,
    get_employee_list,
)


logger = structlog.get_logger(__name__)


# ---------------------------------------------------------------------------
# Employee views
# ---------------------------------------------------------------------------


class EmployeeListView(LoginRequiredMixin, ListView):
    template_name = "pages/employee/employee_list.html"
    context_object_name = "employees"
    paginate_by = 25

    def get_queryset(self):
        qs = get_employee_list()
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(employee_id__icontains=q)
            )
        dept = self.request.GET.get("department", "").strip()
        if dept:
            qs = qs.filter(employment__department_id=dept)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["search_query"] = self.request.GET.get("q", "")
        ctx["departments"] = Department.objects.order_by("name")
        ctx["selected_dept"] = self.request.GET.get("department", "")
        return ctx


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    template_name = "pages/employee/employee_detail.html"
    context_object_name = "employee"

    def get_object(self, queryset=None):
        return get_employee(self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["emergency_contacts"] = get_emergency_contacts_for_employee(self.object.pk)
        return ctx


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    template_name = "pages/employee/employee_form.html"
    fields = [
        "employee_id",
        "first_name",
        "last_name",
        "date_of_birth",
        "gender",
        "nationality",
        "national_id",
        "phone",
        "personal_email",
        "address_line_1",
        "address_line_2",
        "city",
        "state_province",
        "postal_code",
        "country",
        "photo",
    ]

    def get_success_url(self):
        return reverse_lazy("employee:employee-detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form) -> HttpResponse:
        response = super().form_valid(form)
        logger.info("employee.created", employee_id=self.object.employee_id, name=self.object.full_name)
        messages.success(self.request, f"Employee \"{self.object.full_name}\" created successfully.")
        return response


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "pages/employee/employee_form.html"
    fields = [
        "first_name",
        "last_name",
        "date_of_birth",
        "gender",
        "nationality",
        "national_id",
        "phone",
        "personal_email",
        "address_line_1",
        "address_line_2",
        "city",
        "state_province",
        "postal_code",
        "country",
        "photo",
    ]

    def get_object(self, queryset=None):
        return get_employee(self.kwargs["pk"])

    def get_success_url(self):
        return reverse_lazy("employee:employee-detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form) -> HttpResponse:
        response = super().form_valid(form)
        logger.info("employee.updated", employee_id=self.object.employee_id, name=self.object.full_name)
        messages.success(self.request, f"Profile for \"{self.object.full_name}\" updated.")
        return response


class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "pages/employee/employee_confirm_delete.html"
    success_url = reverse_lazy("employee:employee-list")

    def get_object(self, queryset=None):
        return get_employee(self.kwargs["pk"])

    def form_valid(self, form) -> HttpResponse:
        logger.info("employee.deleted", employee_id=self.object.employee_id, name=self.object.full_name)
        messages.success(self.request, f"Employee \"{self.object.full_name}\" removed.")
        return super().form_valid(form)


# ---------------------------------------------------------------------------
# EmergencyContact views
# ---------------------------------------------------------------------------


class EmergencyContactCreateView(LoginRequiredMixin, CreateView):
    model = EmergencyContact
    template_name = "pages/employee/emergencycontact_form.html"
    fields = ["name", "relationship", "phone", "email", "address", "is_primary"]

    def _get_employee(self) -> Employee:
        return get_employee(self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["employee"] = self._get_employee()
        return ctx

    def form_valid(self, form) -> HttpResponse:
        employee = self._get_employee()
        form.instance.employee = employee
        response = super().form_valid(form)
        logger.info("emergency_contact.created", employee_id=str(employee.pk), contact=self.object.name)
        messages.success(self.request, f"Emergency contact \"{self.object.name}\" added.")
        return response

    def get_success_url(self):
        return reverse_lazy("employee:employee-detail", kwargs={"pk": self.kwargs["pk"]})


class EmergencyContactUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "pages/employee/emergencycontact_form.html"
    fields = ["name", "relationship", "phone", "email", "address", "is_primary"]

    def get_object(self, queryset=None):
        return get_emergency_contact(pk=self.kwargs["ec_pk"], employee_pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["employee"] = get_employee(self.kwargs["pk"])
        return ctx

    def get_success_url(self):
        return reverse_lazy("employee:employee-detail", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form) -> HttpResponse:
        response = super().form_valid(form)
        logger.info("emergency_contact.updated", contact_id=str(self.object.pk), contact=self.object.name)
        messages.success(self.request, f"Emergency contact \"{self.object.name}\" updated.")
        return response


class EmergencyContactDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "pages/employee/emergencycontact_confirm_delete.html"

    def get_object(self, queryset=None):
        return get_emergency_contact(pk=self.kwargs["ec_pk"], employee_pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["employee"] = get_employee(self.kwargs["pk"])
        return ctx

    def get_success_url(self):
        return reverse_lazy("employee:employee-detail", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form) -> HttpResponse:
        logger.info("emergency_contact.deleted", contact_id=str(self.object.pk), contact=self.object.name)
        messages.success(self.request, f"Emergency contact \"{self.object.name}\" removed.")
        return super().form_valid(form)
