import contextlib

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View
import structlog

from .models import CompanyProfile
from .services import get_or_create_company_profile, update_company_profile


logger = structlog.get_logger(__name__)

_PROFILE_FIELDS = [
    "name",
    "legal_name",
    "tax_id",
    "registration_number",
    "industry",
    "founded",
    "logo",
    "email",
    "phone",
    "website",
    "linkedin",
    "instagram",
    "twitter",
    "address_street",
    "address_city",
    "address_state",
    "address_postal_code",
    "address_country",
    "work_hours_per_week",
    "probation_days",
    "annual_leave_days",
    "sick_leave_days",
    "default_currency",
    "payroll_cycle",
    "employee_id_format",
    "timezone",
]


class SettingsIndexView(LoginRequiredMixin, View):
    template_name = "settings/index.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        profile = get_or_create_company_profile()
        return render(
            request,
            self.template_name,
            {
                "profile": profile,
                "active_group": "settings",
                "breadcrumbs": [{"label": "Settings", "url": None}],
            },
        )


class CompanyProfileUpdateView(LoginRequiredMixin, View):
    template_name = "settings/company_profile.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        profile = get_or_create_company_profile()
        return self._render(request, profile)

    def post(self, request: HttpRequest) -> HttpResponse:
        profile = get_or_create_company_profile()
        cleaned: dict = {}

        for field in _PROFILE_FIELDS:
            if field == "logo":
                if "logo" in request.FILES:
                    cleaned["logo"] = request.FILES["logo"]
                elif request.POST.get("logo_clear") == "1":
                    cleaned["logo"] = None
                continue

            value = request.POST.get(field, "")
            model_field = CompanyProfile._meta.get_field(field)
            if hasattr(model_field, "to_python"):
                with contextlib.suppress(Exception):
                    value = model_field.to_python(value)
            cleaned[field] = value

        update_company_profile(profile, cleaned)
        messages.success(request, "Company profile updated successfully.")
        return redirect(reverse("settings:company-profile"))

    def _render(self, request: HttpRequest, profile: CompanyProfile) -> HttpResponse:
        return render(
            request,
            self.template_name,
            {
                "profile": profile,
                "payroll_choices": [
                    ("weekly", "Weekly"),
                    ("bi_weekly", "Bi-Weekly"),
                    ("monthly", "Monthly"),
                    ("annual", "Annual"),
                ],
                "active_group": "settings",
                "breadcrumbs": [
                    {"label": "Settings", "url": reverse("settings:index")},
                    {"label": "Company Profile", "url": None},
                ],
            },
        )
