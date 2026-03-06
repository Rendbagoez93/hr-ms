from django.db import models
from django.utils.translation import gettext_lazy as _

from shared.base_models import BaseModel


class EmploymentStatus(models.TextChoices):
    FULL_TIME = "full_time", _("Full Time")
    PART_TIME = "part_time", _("Part Time")
    CONTRACT = "contract", _("Contract")
    INTERN = "intern", _("Intern")
    PROBATION = "probation", _("Probation")


class WorkLocationType(models.TextChoices):
    ON_SITE = "on_site", _("On Site")
    REMOTE = "remote", _("Remote")
    HYBRID = "hybrid", _("Hybrid")


class EmploymentDetailQuerySet(models.QuerySet["EmploymentDetail"]):
    def active(self) -> "EmploymentDetailQuerySet":
        return self.filter(is_active=True)

    def with_relations(self) -> "EmploymentDetailQuerySet":
        return self.select_related("employee", "department", "job_title", "reporting_manager")


class EmploymentDetail(BaseModel):
    employee = models.OneToOneField(
        "employee.Employee",
        on_delete=models.CASCADE,
        related_name="employment_detail",
        verbose_name=_("employee"),
    )
    department = models.ForeignKey(
        "department.Department",
        on_delete=models.PROTECT,
        related_name="employees",
        verbose_name=_("department"),
    )
    job_title = models.ForeignKey(
        "job_title.JobTitle",
        on_delete=models.PROTECT,
        related_name="employees",
        verbose_name=_("job title"),
    )
    work_location = models.CharField(_("work location"), max_length=200, blank=True, default="")
    work_location_type = models.CharField(
        _("work location type"),
        max_length=20,
        choices=WorkLocationType.choices,
        default=WorkLocationType.ON_SITE,
    )
    employment_status = models.CharField(
        _("employment status"),
        max_length=20,
        choices=EmploymentStatus.choices,
        default=EmploymentStatus.FULL_TIME,
    )
    start_date = models.DateField(_("start date"))
    reporting_manager = models.ForeignKey(
        "employee.Employee",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="direct_reports",
        verbose_name=_("reporting manager"),
    )

    objects = EmploymentDetailQuerySet.as_manager()

    class Meta:
        verbose_name = _("employment detail")
        verbose_name_plural = _("employment details")

    def __str__(self) -> str:
        return f"{self.employee} — {self.job_title} ({self.department})"
