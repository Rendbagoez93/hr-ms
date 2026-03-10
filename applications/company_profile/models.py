from django.db import models
from django.utils.translation import gettext_lazy as _

from shared.base_models import BaseModel


class CompanyProfile(BaseModel):
    """
    Singleton-like model storing the company's identity and configuration.
    Only one active record is expected (enforced at the service layer).
    """

    # Identity
    name = models.CharField(_("company name"), max_length=200)
    legal_name = models.CharField(_("legal name"), max_length=200, blank=True)
    tax_id = models.CharField(_("tax ID"), max_length=50, blank=True)
    registration_number = models.CharField(_("registration number"), max_length=100, blank=True)
    industry = models.CharField(_("industry"), max_length=100, blank=True)
    founded = models.CharField(_("founded year"), max_length=10, blank=True)
    logo = models.ImageField(_("logo"), upload_to="company/logo/", null=True, blank=True)

    # Contact
    email = models.EmailField(_("email"), blank=True)
    phone = models.CharField(_("phone"), max_length=50, blank=True)
    website = models.URLField(_("website"), blank=True)

    # Social media
    linkedin = models.URLField(_("LinkedIn"), blank=True)
    instagram = models.URLField(_("Instagram"), blank=True)
    twitter = models.URLField(_("Twitter / X"), blank=True)

    # Address
    address_street = models.CharField(_("street address"), max_length=255, blank=True)
    address_city = models.CharField(_("city"), max_length=100, blank=True)
    address_state = models.CharField(_("state / province"), max_length=100, blank=True)
    address_postal_code = models.CharField(_("postal code"), max_length=20, blank=True)
    address_country = models.CharField(_("country"), max_length=100, blank=True)

    # HR settings
    work_hours_per_week = models.PositiveSmallIntegerField(_("work hours per week"), default=40)
    probation_days = models.PositiveSmallIntegerField(_("probation period (days)"), default=90)
    annual_leave_days = models.PositiveSmallIntegerField(_("annual leave days"), default=12)
    sick_leave_days = models.PositiveSmallIntegerField(_("sick leave days"), default=12)
    default_currency = models.CharField(_("default currency"), max_length=10, default="IDR")
    payroll_cycle = models.CharField(_("payroll cycle"), max_length=30, default="monthly")
    employee_id_format = models.CharField(
        _("employee ID format"),
        max_length=50,
        default="EMP-{YEAR}-{SEQ:04d}",
        help_text="Use {YEAR} and {SEQ:04d} as placeholders.",
    )

    # Timezone
    timezone = models.CharField(_("timezone"), max_length=50, default="Asia/Jakarta")

    class Meta:
        verbose_name = _("Company Profile")
        verbose_name_plural = _("Company Profiles")

    def __str__(self) -> str:
        return self.name
