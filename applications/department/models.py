from django.db import models
from django.utils.translation import gettext_lazy as _

from shared.base_models import BaseModel


class DepartmentQuerySet(models.QuerySet["Department"]):
    def active(self) -> "DepartmentQuerySet":
        return self.filter(is_active=True)


class Department(BaseModel):
    name = models.CharField(_("name"), max_length=100, unique=True)
    description = models.TextField(_("description"), blank=True, default="")

    objects = DepartmentQuerySet.as_manager()

    class Meta:
        verbose_name = _("department")
        verbose_name_plural = _("departments")
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
