from django.db import models
from django.utils.translation import gettext_lazy as _

from shared.base_models import BaseModel


class ContractType(models.TextChoices):
    PERMANENT = "permanent", _("Permanent")
    FIXED_TERM = "fixed_term", _("Fixed Term")
    FREELANCE = "freelance", _("Freelance")
    INTERNSHIP = "internship", _("Internship")


class ContractQuerySet(models.QuerySet["Contract"]):
    def active(self) -> "ContractQuerySet":
        return self.filter(is_active=True)

    def for_employee(self, employee_id) -> "ContractQuerySet":
        return self.filter(employee_id=employee_id)


class Contract(BaseModel):
    employee = models.ForeignKey(
        "employee.Employee",
        on_delete=models.CASCADE,
        related_name="contracts",
        verbose_name=_("employee"),
    )
    contract_type = models.CharField(
        _("contract type"),
        max_length=20,
        choices=ContractType.choices,
        default=ContractType.PERMANENT,
    )
    start_date = models.DateField(_("start date"))
    end_date = models.DateField(_("end date"), null=True, blank=True)
    terms = models.TextField(_("terms"), blank=True, default="")

    objects = ContractQuerySet.as_manager()

    class Meta:
        verbose_name = _("contract")
        verbose_name_plural = _("contracts")
        ordering = ["-start_date"]

    def __str__(self) -> str:
        return f"{self.employee} ({self.contract_type})"
