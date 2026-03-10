from django.db import models
from django.utils.translation import gettext_lazy as _

from applications.employee.models import Employee
from applications.organization.models import Department, JobTitle
from shared.base_models import BaseModel

from .constants import ContractType, EmploymentStatus, PaymentFrequency, WorkLocationType
from .managers import ContractManager, EmploymentManager, SalaryManager


class Employment(BaseModel):
    """Links an employee to a position, department, and work arrangement."""

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name="employment",
        verbose_name=_("employee"),
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="employments",
        verbose_name=_("department"),
    )
    job_title = models.ForeignKey(
        JobTitle,
        on_delete=models.PROTECT,
        related_name="employments",
        verbose_name=_("job title"),
    )
    reporting_manager = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="direct_reports",
        verbose_name=_("reporting manager"),
    )
    work_location = models.CharField(
        _("work location"),
        max_length=20,
        choices=WorkLocationType.choices(),
        default=WorkLocationType.ONSITE,
    )
    status = models.CharField(
        _("status"),
        max_length=20,
        choices=EmploymentStatus.choices(),
        default=EmploymentStatus.PROBATION,
    )
    hire_date = models.DateField(_("hire date"))
    end_date = models.DateField(_("end date"), null=True, blank=True)

    objects = EmploymentManager()

    class Meta:
        verbose_name = _("Employment")
        verbose_name_plural = _("Employments")
        ordering = ("-hire_date",)

    def __str__(self) -> str:
        return f"{self.employee} — {self.job_title} @ {self.department}"


class Contract(BaseModel):
    """Employment contract attached to an employment record."""

    employment = models.ForeignKey(
        Employment,
        on_delete=models.CASCADE,
        related_name="contracts",
        verbose_name=_("employment"),
    )
    contract_type = models.CharField(
        _("contract type"),
        max_length=30,
        choices=ContractType.choices(),
    )
    start_date = models.DateField(_("start date"))
    end_date = models.DateField(_("end date"), null=True, blank=True)
    terms = models.TextField(_("terms"), blank=True)
    document = models.FileField(_("document"), upload_to="contracts/", null=True, blank=True)

    objects = ContractManager()

    class Meta:
        verbose_name = _("Contract")
        verbose_name_plural = _("Contracts")
        ordering = ("-start_date",)

    def __str__(self) -> str:
        return f"{self.employment.employee} — {self.contract_type} ({self.start_date})"


class Salary(BaseModel):
    """Salary record representing a pay rate for a given period."""

    employment = models.ForeignKey(
        Employment,
        on_delete=models.CASCADE,
        related_name="salary_history",
        verbose_name=_("employment"),
    )
    pay_grade = models.CharField(_("pay grade"), max_length=20, blank=True)
    amount = models.DecimalField(_("amount"), max_digits=14, decimal_places=2)
    currency = models.CharField(_("currency"), max_length=10, default="IDR")
    payment_frequency = models.CharField(
        _("payment frequency"),
        max_length=20,
        choices=PaymentFrequency.choices(),
        default=PaymentFrequency.MONTHLY,
    )
    effective_date = models.DateField(_("effective date"))
    end_date = models.DateField(_("end date"), null=True, blank=True)
    notes = models.TextField(_("notes"), blank=True)

    objects = SalaryManager()

    class Meta:
        verbose_name = _("Salary")
        verbose_name_plural = _("Salaries")
        ordering = ("-effective_date",)

    def __str__(self) -> str:
        return f"{self.employment.employee} — {self.amount} {self.currency} ({self.effective_date})"
