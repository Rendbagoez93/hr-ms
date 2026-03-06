from django.db import models
from django.utils.translation import gettext_lazy as _

from shared.base_models import BaseModel


class EmergencyContactQuerySet(models.QuerySet["EmergencyContact"]):
    def for_employee(self, employee_id) -> "EmergencyContactQuerySet":
        return self.filter(employee_id=employee_id)


class EmergencyContact(BaseModel):
    employee = models.ForeignKey(
        "employee.Employee",
        on_delete=models.CASCADE,
        related_name="emergency_contacts",
        verbose_name=_("employee"),
    )
    name = models.CharField(_("name"), max_length=100)
    relationship = models.CharField(_("relationship"), max_length=50)
    phone_number = models.CharField(_("phone number"), max_length=20)
    address = models.TextField(_("address"), blank=True, default="")

    objects = EmergencyContactQuerySet.as_manager()

    class Meta:
        verbose_name = _("emergency contact")
        verbose_name_plural = _("emergency contacts")
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.relationship}) — {self.employee}"
