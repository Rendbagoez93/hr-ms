from django.db import models
from django.utils.translation import gettext_lazy as _

from shared.base_models import BaseModel

from .managers import DepartmentManager, JobTitleManager


class Department(BaseModel):
    """An organisational unit within the company (e.g. Engineering, Sales, HR)."""

    name = models.CharField(_("name"), max_length=150, unique=True)
    code = models.CharField(_("code"), max_length=20, unique=True)
    description = models.TextField(_("description"), blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
        verbose_name=_("parent department"),
    )

    objects = DepartmentManager()

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class JobTitle(BaseModel):
    """A specific role or position within the company (e.g. Software Engineer)."""

    name = models.CharField(_("name"), max_length=150)
    code = models.CharField(_("code"), max_length=20, unique=True)
    description = models.TextField(_("description"), blank=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="job_titles",
        verbose_name=_("department"),
    )

    objects = JobTitleManager()

    class Meta:
        verbose_name = _("Job Title")
        verbose_name_plural = _("Job Titles")
        ordering = ("name",)
        constraints = (
            models.UniqueConstraint(
                fields=["name", "department"],
                name="unique_job_title_per_department",
            ),
        )

    def __str__(self) -> str:
        if self.department:
            return f"{self.name} ({self.department.name})"
        return self.name
