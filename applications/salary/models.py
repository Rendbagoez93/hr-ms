from django.db import models
from django.utils.translation import gettext_lazy as _

from shared.base_models import BaseModel


class PaymentFrequency(models.TextChoices):
    MONTHLY = "monthly", _("Monthly")
    WEEKLY = "weekly", _("Weekly")
    BI_WEEKLY = "bi_weekly", _("Bi-Weekly")
    ANNUAL = "annual", _("Annual")


class SalaryQuerySet(models.QuerySet["Salary"]):
    def active(self) -> "SalaryQuerySet":
        return self.filter(is_active=True)

    def for_employee(self, employee_id) -> "SalaryQuerySet":
        return self.filter(employee_id=employee_id)

    def latest_per_employee(self) -> "SalaryQuerySet":
        return self.order_by("employee", "-effective_date").distinct("employee")


class Salary(BaseModel):
    employee = models.ForeignKey(
        "employee.Employee",
        on_delete=models.CASCADE,
        related_name="salaries",
        verbose_name=_("employee"),
    )
    pay_grade = models.CharField(_("pay grade"), max_length=50, blank=True, default="")
    amount = models.DecimalField(_("amount"), max_digits=14, decimal_places=2)
    currency = models.CharField(_("currency"), max_length=3, default="IDR")
    frequency = models.CharField(
        _("frequency"),
        max_length=20,
        choices=PaymentFrequency.choices,
        default=PaymentFrequency.MONTHLY,
    )
    effective_date = models.DateField(_("effective date"))

    objects = SalaryQuerySet.as_manager()

    class Meta:
        verbose_name = _("salary")
        verbose_name_plural = _("salaries")
        ordering = ["-effective_date"]

    def __str__(self) -> str:
        return f"{self.employee} — {self.amount} {self.currency} ({self.frequency})"
